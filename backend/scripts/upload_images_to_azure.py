import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient, ContentSettings


def guess_content_type(suffix: str) -> str:
    ext = suffix.lower()
    if ext in {'.jpg', '.jpeg'}:
        return 'image/jpeg'
    if ext == '.png':
        return 'image/png'
    if ext == '.gif':
        return 'image/gif'
    return 'application/octet-stream'


def upload_images(images_dir: Path, container: str, connection_string: str) -> None:
    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client(container)
    container_client.create_container()

    for image_path in images_dir.iterdir():
        if not image_path.is_file():
            continue
        blob_client = container_client.get_blob_client(image_path.name)
        with image_path.open('rb') as fh:
            blob_client.upload_blob(
                fh,
                overwrite=True,
                content_settings=ContentSettings(
                    content_type=guess_content_type(image_path.suffix)
                ),
            )
        print(f'Uploaded {image_path.name}')


def main() -> None:
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    if not connection_string:
        print('AZURE_STORAGE_CONNECTION_STRING env var is required')
        return
    container = os.getenv('AZURE_STORAGE_CONTAINER', 'images')
    images_dir = Path(__file__).resolve().parents[1] / 'project_store' / 'images'
    upload_images(images_dir, container, connection_string)


if __name__ == '__main__':
    main()
