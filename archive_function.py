import logging
import datetime
import azure.functions as func
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient
import json
import os

# Cosmos DB settings
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
COSMOS_DB_NAME = os.environ["COSMOS_DB_NAME"]
COSMOS_CONTAINER_NAME = os.environ["COSMOS_CONTAINER_NAME"]

# Blob storage settings
BLOB_CONNECTION_STRING = os.environ["BLOB_CONNECTION_STRING"]
BLOB_CONTAINER_NAME = os.environ["BLOB_CONTAINER_NAME"]

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    logging.info(f"Archive function triggered at {utc_timestamp}")

    try:
        # Set up Cosmos client
        cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
        db = cosmos_client.get_database_client(COSMOS_DB_NAME)
        container = db.get_container_client(COSMOS_CONTAINER_NAME)

        # Set up Blob client
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_container = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        if not blob_container.exists():
            blob_container.create_container()

        # Get current date and compute cutoff
        now = datetime.datetime.utcnow()
        cutoff_date = now - datetime.timedelta(days=90)

        # Query for old records
        query = "SELECT * FROM c WHERE c.timestamp < @cutoff"
        parameters = [{"name": "@cutoff", "value": cutoff_date.isoformat()}]
        items = list(container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        if not items:
            logging.info("No records found older than 3 months.")
            return

        # Archive and delete
        for item in items:
            blob_name = f"{item['id']}.json"
            blob_data = json.dumps(item)
            blob_container.upload_blob(name=blob_name, data=blob_data, overwrite=True)
            container.delete_item(item=item['id'], partition_key=item['partitionKey'])

        logging.info(f"Archived and deleted {len(items)} records.")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
