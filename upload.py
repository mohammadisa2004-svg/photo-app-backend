from azure.storage.blob import BlobServiceClient
import uuid

# Replace with your actual Storage Account info
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=photossstorage;AccountKey=00rutLZHKcnZVt5ZPh1hXr6zofT2zj7endOw/x5XlA0kQBlyw2/cGuKuyu35cq0At03n2393ld61+AStHX3jwg==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "photos"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_image(file):
    """
    Upload a file to Azure Blob Storage and return its URL
    """
    blob_name = f"{uuid.uuid4()}-{file.filename}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file, overwrite=True)
    return blob_client.url