import zipfile


def read_archive_file(
    zip_file: zipfile.ZipFile,
    file_name: str,
) -> str:
    with zip_file.open(file_name) as f:
        file_content = f.read().decode("utf-8")
    return file_content
