from src import gdrive
from src.testing import external_api

import json
from requests_toolbelt.multipart import decoder
from unittest import mock

gdrive_file_path = "src.gdrive"

access_token = "access_token"

image_name = "image_name"
image_bytes = b"image-bytes"
parent_folder_id = "parent-folder-123"

image_drive_id = "image-id-123"
image_md5_checksum = "image-md5-checksum"


class UploadSmallJpegRequestHandler(
    external_api.WebRequestHandler,
):

    def do_POST(self):
        # verifying the request
        assert (
            self.url.path == "/upload/drive/v3/files"
        ), "Request made to incorrect path"
        assert (
            self.query_data["uploadType"] == "multipart"
        ), "Request should have query param specifying uploadType to be multipart"
        assert (
            self.query_data["supportsAllDrives"] == "True"
        ), "Request should have query param specifying supportsAllDrives to be True (needed for shared drives upload)"
        assert (
            self.headers.get("Authorization") == f"Bearer {access_token}"
        ), f"Access token not provided in authorization header, got: {self.headers.get("Authorization")}"
        request_body = decoder.MultipartDecoder(
            self.post_data,
            self.headers["Content-Type"],
        )
        request_metadata: gdrive.ImageMetadata | None = None
        request_image_bytes: bytes | None
        for part in request_body.parts:
            content_type = part.headers[b"Content-Type"].decode()
            if content_type == "application/json; charset=UTF-8":
                request_metadata = json.loads(part.text)
            elif content_type == "image/jpeg":
                request_image_bytes = part.content
            else:
                raise Exception(
                    f"Unexpected request body part: {part.headers}; {part.text}"
                )
        if request_metadata is None:
            raise Exception("Failed to extract metadata from request")
        if request_image_bytes is None:
            raise Exception("Failed to extract image bytes from request")
        assert (
            request_image_bytes == image_bytes
        ), f"Different bytes sent to server, expected {image_bytes}, got {request_image_bytes}"
        assert request_metadata["parents"] == [
            parent_folder_id
        ], f"Upload folder was incorrect, expected {[parent_folder_id]}, got {request_metadata["parents"]}"
        assert (
            request_metadata["name"] == image_name
        ), f"Image name was incorrect, expected {image_name}, got {request_metadata["name"]}"
        assert (
            request_metadata["mimeType"] == "image/jpeg"
        ), f"Mime type was incorrect, expected image/jpeg, got {request_metadata["mimeType"]}"
        # building response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_content = json.dumps(
            {"id": image_drive_id, "md5Checksum": image_md5_checksum}
        )
        self.wfile.write(bytes(response_content, "utf-8"))


@mock.patch(
    f"{gdrive_file_path}._get_gdrive_access_token",
    return_value=access_token,
    name="get gdrive access token",
)
class UploadSmallJpegTests(
    external_api.ExternalApiTestCase,
):
    RequestHandlerClass = UploadSmallJpegRequestHandler

    def test_upload(self, _) -> None:
        with mock.patch(
            f"{gdrive_file_path}.GOOGLE_APIS_URL",
            self.test_server_base_url,
        ):
            gdrive_client = gdrive.GDriveClient()
            try:
                file_data = gdrive.upload_small_jpeg(
                    gdrive_client,
                    image_name,
                    [parent_folder_id],
                    image_bytes,
                )
            except:
                self.fail(
                    f"{self.RequestHandlerClass.__name__} raised, please investigate "
                    "traceback."
                )
            self.assertEqual(file_data.id, image_drive_id)
            self.assertEqual(file_data.md5_checksum, image_md5_checksum)


class TrashFileExternalApiRequestHandler(
    external_api.WebRequestHandler,
):

    def do_PATCH(self):
        # verifying the request
        assert (
            self.url.path == f"/drive/v3/files/{image_drive_id}"
        ), "Request made to incorrect path"
        assert (
            self.query_data["supportsAllDrives"] == "True"
        ), "Request should have query param specifying supportsAllDrives to be True (needed for shared drives operations)"
        assert (
            self.headers.get("Authorization") == f"Bearer {access_token}"
        ), f"Access token not provided in authorization header, got: {self.headers.get("Authorization")}"
        assert self.json[
            "trashed"
        ], '"trashed" should be true in the json posted to gdrive to trash a file'
        # building response
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()


@mock.patch(
    f"{gdrive_file_path}._get_gdrive_access_token",
    return_value=access_token,
    name="get gdrive access token",
)
class TrashFileExternalApiTests(
    external_api.ExternalApiTestCase,
):
    RequestHandlerClass = TrashFileExternalApiRequestHandler

    def test_delete(self, _) -> None:
        with mock.patch(
            f"{gdrive_file_path}.GOOGLE_APIS_URL",
            self.test_server_base_url,
        ):
            gdrive_client = gdrive.GDriveClient()
            try:
                gdrive.trash_file(
                    gdrive_client,
                    image_drive_id,
                )
            except:
                self.fail(
                    f"{self.RequestHandlerClass.__name__} raised, please investigate "
                    "traceback."
                )


# class DeleteFileExternalApiRequestHandler(
#     external_api.WebRequestHandler,
# ):

#     def do_DELETE(self):
#         # verifying the request
#         assert (
#             self.url.path == f"/drive/v3/files/{image_drive_id}"
#         ), "Request made to incorrect path"
#         assert (
#             self.query_data["supportsAllDrives"] == "True"
#         ), "Request should have query param specifying supportsAllDrives to be True (needed for shared drives operations)"
#         assert (
#             self.headers.get("Authorization") == f"Bearer {access_token}"
#         ), f"Access token not provided in authorization header, got: {self.headers.get("Authorization")}"
#         # building response
#         self.send_response(200)
#         self.send_header("Content-Type", "text/plain")
#         self.end_headers()


# @mock.patch(
#     f"{gdrive_file_path}._get_gdrive_access_token",
#     return_value=access_token,
#     name="get gdrive access token",
# )
# class DeleteFileExternalApiTests(
#     external_api.ExternalApiTestCase,
# ):
#     RequestHandlerClass = DeleteFileExternalApiRequestHandler

#     def test_delete(self, _) -> None:
#         with mock.patch(
#             f"{gdrive_file_path}.GOOGLE_APIS_URL",
#             self.test_server_base_url,
#         ):
#             gdrive_client = gdrive.GDriveClient()
#             try:
#                 gdrive.delete_file(
#                     gdrive_client,
#                     image_drive_id,
#                 )
#             except:
#                 self.fail(
#                     f"{self.RequestHandlerClass.__name__} raised, please investigate "
#                     "traceback."
#                 )
