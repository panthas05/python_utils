from django.conf import settings

import base64
import io
import json
import requests
import time
from typing import Any, Protocol, TypedDict
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata, choose_boundary

from src import (
    google_apis,
    inter_process_lock,
    requests as requests_utils,
)


GDRIVE_ACCESS_TOKEN_CACHE_KEY = "gdrive-auth-token-key"

GOOGLE_APIS_URL = "https://www.googleapis.com"


def _get_gdrive_access_token(
    service_account_email: str,
    private_key: str,
) -> str:
    return google_apis.get_access_token(
        service_account_email,
        ["https://www.googleapis.com/auth/drive"],
        private_key,
        GDRIVE_ACCESS_TOKEN_CACHE_KEY,
    )


class GDriveClient:

    auth_token: str | None = None

    auth_lock = inter_process_lock.InterProcessLock("gdrive-auth-lock")
    rate_lock = inter_process_lock.InterProcessLock("gdrive-rate-lock")

    last_get_times: list[float] = []

    session = requests.Session()

    def __init__(
        self,
        service_account_email: str,
        private_key: str,
    ) -> None:
        self.service_account_email = service_account_email
        self.private_key = private_key

    def authenticate(self) -> None:
        with self.auth_lock:
            if self.auth_token is None:
                self.auth_token = _get_gdrive_access_token(
                    self.service_account_email,
                    self.private_key,
                )
                if not self.auth_token:
                    raise Exception("Could not authenticate!" + str(self.auth_token))

    def limit_rate(self) -> None:
        with self.rate_lock:
            if len(self.last_get_times) >= 8:
                elapsed = time.time() - self.last_get_times[-8]
                time.sleep(max(1 - elapsed, 0))
            self.last_get_times.append(time.time())

    def _send_request(
        self,
        request: requests.Request,
        timeout: int,
    ) -> requests.Response:
        self.limit_rate()

        if self.auth_token is None:
            raise Exception(
                'Please call the "authenticate" method before making any requests'
            )

        headers = {
            **request.headers,
            "Authorization": "Bearer " + self.auth_token,
        }
        request.headers = headers

        prepared_request = request.prepare()
        response = self.session.send(
            prepared_request,
            timeout=timeout,
        )

        return response

    def send_request(
        self,
        request: requests.Request,
        timeout: int = 300,
        **kwargs: Any,
    ) -> requests.Response:
        self.authenticate()

        response = self._send_request(
            request,
            timeout,
            **kwargs,
        )

        if response.status_code == 401:
            # reauthenticating
            self.auth_token = None
            self.authenticate()
            response = self._send_request(
                request,
                timeout,
                **kwargs,
            )
            if response.status_code == 401:
                raise Exception(
                    f"{request.method} request to {request.url} couldn't authenticate "
                    f"- response body: {response.content.decode()}"
                )
        requests_utils.informative_raise_for_status(response)

        return response


class MultipartRelatedRequestData:
    body: bytes
    content_type: str

    def __init__(
        self,
        body: bytes,
        content_type: str,
    ) -> None:
        self.body = body
        self.content_type = content_type


def _encode_multipart_related(
    fields: list[RequestField],
) -> MultipartRelatedRequestData:
    boundary = choose_boundary()

    body, _ = encode_multipart_formdata(fields, boundary)
    content_type = f"multipart/related; boundary={boundary}"

    return MultipartRelatedRequestData(body, content_type)


class ImageMetadata(TypedDict):
    name: str
    parents: list[str]
    mimeType: str


def _build_upload_small_jpeg_body(
    metadata: ImageMetadata,
    image_bytes: bytes,
) -> MultipartRelatedRequestData:
    fields = [
        RequestField(
            name="metadata",
            data=json.dumps(metadata),
            headers={"Content-Type": "application/json; charset=UTF-8"},
        ),
        RequestField(
            name="media",
            data=image_bytes,
            headers={"Content-Type": "image/jpeg"},
        ),
    ]
    return _encode_multipart_related(fields)


class GDriveFile:

    def __init__(
        self,
        file_id: str,
        md5_checksum: str,
    ) -> None:
        self.id = file_id
        self.md5_checksum = md5_checksum


def upload_small_jpeg(
    client: GDriveClient,
    name: str,
    parents: list[str],
    image_bytes: bytes,
) -> GDriveFile:

    image_metadata: ImageMetadata = {
        "name": name,
        "parents": parents,
        "mimeType": "image/jpeg",
    }
    request_data = _build_upload_small_jpeg_body(
        image_metadata,
        image_bytes,
    )
    request = requests.Request(
        method="POST",
        url=f"{GOOGLE_APIS_URL}/upload/drive/v3/files",
        data=request_data.body,
        params={
            "uploadType": "multipart",
            "supportsAllDrives": True,  # needed to upload to a shared drive(?)
            "fields": "id, md5Checksum",
        },
        headers={
            "Content-Type": request_data.content_type,
        },
    )
    response = client.send_request(request)
    response_json = response.json()

    return GDriveFile(
        file_id=response_json["id"],
        md5_checksum=response_json["md5Checksum"],
    )


def trash_file(
    client: GDriveClient,
    file_id: str,
) -> None:
    request = requests.Request(
        method="PATCH",
        url=f"{GOOGLE_APIS_URL}/drive/v3/files/{file_id}",
        params={
            "supportsAllDrives": True,  # needed to update a file in a shared drive(?)
        },
        json={
            "trashed": True,
        },
    )
    response = client.send_request(request)


# def delete_file(
#     client: GDriveClient,
#     file_id: str,
# ) -> None:
#     request = requests.Request(
#         method="DELETE",
#         url=f"{GOOGLE_APIS_URL}/drive/v3/files/{file_id}",
#         params={
#             "supportsAllDrives": True,  # needed to delete from a shared drive(?)
#         },
#     )
#     response = client.send_request(request)
#     assert (
#         response.content.decode() == ""
#     ), "Was expecting an empty response body for a successful request"
