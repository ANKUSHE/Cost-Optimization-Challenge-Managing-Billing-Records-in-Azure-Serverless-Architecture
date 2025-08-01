import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import json

# Blob storage settings
BLOB_CONNECTION_STRING = os.environ["BLOB_CONNECTION_STRING"]
BLOB_CONTAINER_NAME = os.environ["BLOB_CONTAINER_NAME"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Read function triggered.")

    try:
        # Set up Blob client
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

        if not container_client.exists():
            return func.HttpResponse("Blob container does not exist.", status_code=404)

        # List blobs
        blobs = container_client.list_blobs()
        results = []

        for blob in blobs:
            blob_client = container_client.get_blob_client(blob)
            data = blob_client.download_blob().readall()
            record = json.loads(data)
            results.append(record)

        return func.HttpResponse(json.dumps(results, indent=2), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.error(f"Error reading from Blob: {e}")
        return func.HttpResponse("Error reading archived data.", status_code=500)
