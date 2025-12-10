from unittest import mock, TestCase

from . import django_test_case
from src.django import file_storage

from io import BytesIO


class HashNameFileStorageTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    hashNameFileStorage = file_storage.HashNameFileStorage()
    content = b"aaaaaaaa"

    def _get_hash_from_filename(self, filename: str) -> str:
        filename_bits = filename.split(".")
        self.assertEqual(len(filename_bits), 3)
        return filename_bits[1]

    @mock.patch("django.core.files.storage.FileSystemStorage.save", autospec=True)
    def test_generates_hash(self, mock_save):
        self.hashNameFileStorage.save("foo.txt", BytesIO(self.content))
        mock_save.assert_called_once()
        _, filename, bytesio = mock_save.call_args.args
        # checking name had hash inserted
        self.assertEqual(len(self._get_hash_from_filename(filename)), 8)
        # checking content passed through unmodified
        self.assertEqual(bytesio.read(), self.content)

    @mock.patch("django.core.files.storage.FileSystemStorage.save", autospec=True)
    def test_generates_differing_hashes(self, mock_save):
        self.hashNameFileStorage.save("foo.txt", BytesIO(self.content))
        self.hashNameFileStorage.save("foo.txt", BytesIO(self.content + b"a"))
        self.assertEqual(len(mock_save.call_args_list), 2)
        [(_, first_filename, _), (_, second_filename, _)] = [
            c.args for c in mock_save.call_args_list
        ]
        first_hash = self._get_hash_from_filename(first_filename)
        second_hash = self._get_hash_from_filename(second_filename)
        self.assertNotEqual(first_hash, second_hash)
