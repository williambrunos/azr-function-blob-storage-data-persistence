import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

os.environ['AZR_STORAGE_ACCOUNT_CONNECTION_KEY'] = os.getenv('AZR_STORAGE_ACCOUNT_CONNECTION_KEY')


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="azr_function_blob_persistence")
def azr_function_blob_persistence(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        connection_string = os.environ['AZR_STORAGE_ACCOUNT_CONNECTION_KEY']
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Create a local directory to hold blob data
        request_as_json = req.get_json()
        request_as_string = json.dumps(request_as_json)
        logging.info(f'request as string: {request_as_string}\n\nType: {type(request_as_string)}')
        
        today_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        local_file_name = f"test-{today_date}.json"
        
        # Create a unique name for the container
        container_name = "test"
        blob_name = f"retro/{local_file_name}"

        # Create the container
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        logging.info("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        blob_client.upload_blob(data=request_as_string, overwrite=False)

        logging.info("Done")
        
        return func.HttpResponse(
                "This HTTP triggered function executed successfully.",
                status_code=200
            )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
                "An internal error ocurred. Please try again later.",
                status_code=500
            )