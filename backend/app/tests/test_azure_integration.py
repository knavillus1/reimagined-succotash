import sys  # Added import
import os  # Added import
import pytest
from fastapi.testclient import TestClient
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import DefaultAzureCredential

# Add project root to sys.path to allow for absolute imports like 'from backend.app.main import app'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app.main import app  # Assuming your FastAPI app instance is named 'app'

# Configuration - Ensure these are set in your environment for testing
AZURE_TABLES_ACCOUNT_URL = os.environ.get("AZURE_TABLES_ACCOUNT_URL")
AZURE_TABLES_TABLE_NAME = os.environ.get("AZURE_TABLES_TABLE_NAME")
AZURE_TABLES_PARTITION = os.environ.get("AZURE_TABLES_PARTITION", "projects")
AZURE_BLOB_STORAGE_ACCOUNT_URL = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT_URL")
AZURE_BLOB_CONTAINER_NAME = os.environ.get("AZURE_BLOB_CONTAINER_NAME", "images")

# Check if essential environment variables are set
SKIP_AZURE_TESTS = not all([AZURE_TABLES_ACCOUNT_URL, AZURE_TABLES_TABLE_NAME, AZURE_BLOB_STORAGE_ACCOUNT_URL])

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def table_service_client():
    if SKIP_AZURE_TESTS:
        pytest.skip("Skipping Azure tests due to missing environment variables.")
    credential = DefaultAzureCredential()
    return TableServiceClient(endpoint=AZURE_TABLES_ACCOUNT_URL, credential=credential)

@pytest.fixture(scope="module")
def blob_service_client():
    if SKIP_AZURE_TESTS:
        pytest.skip("Skipping Azure tests due to missing environment variables.")
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=AZURE_BLOB_STORAGE_ACCOUNT_URL, credential=credential)

@pytest.mark.skipif(SKIP_AZURE_TESTS, reason="Azure environment variables not set")
def test_get_project_from_table_storage(client, table_service_client):
    """
    Test fetching a specific project ('ProjectExample1') from Azure Table Storage.
    """
    table_client = table_service_client.get_table_client(AZURE_TABLES_TABLE_NAME)

    # Check if the entity exists (optional, but good for test reliability)
    try:
        entity = table_client.get_entity(partition_key=AZURE_TABLES_PARTITION, row_key="ProjectExample1")
        assert entity is not None
    except Exception as e:
        pytest.fail(f"Test entity 'ProjectExample1' not found in table storage or error: {e}")

    response = client.get(f"/api/projects/ProjectExample1")
    assert response.status_code == 200
    project_data = response.json()
    assert project_data["id"] == "ProjectExample1"
    assert "title" in project_data
    # Add more assertions based on the expected structure of 'ProjectExample1'

@pytest.mark.skipif(SKIP_AZURE_TESTS, reason="Azure environment variables not set")
def test_get_image_from_blob_storage(client, blob_service_client):
    """
    Test fetching an image ('1.png') from Azure Blob Storage.
    """
    container_client = blob_service_client.get_container_client(AZURE_BLOB_CONTAINER_NAME)
    blob_client = container_client.get_blob_client("1.png")

    # Check if the blob exists (optional, but good for test reliability)
    if not blob_client.exists():
        pytest.fail(f"Test image '1.png' not found in blob container '{AZURE_BLOB_CONTAINER_NAME}'. Ensure it's uploaded.")

    response = client.get(f"/api/images/1.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png" # Or the correct content type
    # Check if content is not empty, or even compare with a local copy if feasible
    assert len(response.content) > 0

@pytest.mark.skipif(SKIP_AZURE_TESTS, reason="Azure environment variables not set")
def test_get_nonexistent_image_from_blob_storage(client):
    """
    Test fetching a non-existent image from Azure Blob Storage.
    """
    response = client.get(f"/api/images/nonexistentimage12345.png")
    assert response.status_code == 404

@pytest.mark.skipif(SKIP_AZURE_TESTS, reason="Azure environment variables not set")
def test_get_nonexistent_project_from_table_storage(client):
    """
    Test fetching a non-existent project from Azure Table Storage.
    """
    response = client.get(f"/api/projects/nonexistentproject12345")
    assert response.status_code == 404

# To run these tests, ensure you have pytest installed (pip install pytest)
# and the necessary Azure environment variables are set.
# You can run them from the root of your 'backend' directory or project root:
# (venv) $ pytest
# or specifically:
# (venv) $ pytest backend/app/tests/test_azure_integration.py
