from django.core.files.storage import FileSystemStorage

from base64 import b32encode
import hashlib
from typing import Any, IO
import os


class HashNameFileStorage(FileSystemStorage):
    def save(
        self,
        name: str | None,
        content: IO[Any],
        max_length: int | None = None,
    ) -> str:
        if isinstance(name, str):
            directory_name, file_name = os.path.split(name)
            file_root, file_extension = os.path.splitext(file_name)

            file_hash = (
                b32encode(hashlib.sha1(content.read()).digest())
                .decode("ascii")
                .lower()[:8]
            )
            name = os.path.join(
                directory_name,
                f"{file_root}.{file_hash}{file_extension}",
            )
            content.seek(0)
            if os.path.exists(self.path(name)):
                os.unlink(self.path(name))
        return super().save(name, content, max_length=max_length)
