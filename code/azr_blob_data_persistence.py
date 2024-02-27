import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

os.environ['AZR_STORAGE_ACCOUNT_CONNECTION_KEY'] = os.getenv('AZR_STORAGE_ACCOUNT_CONNECTION_KEY')

try:
    print("Azure Blob Storage Python quickstart sample")
    connect_str = os.environ['AZR_STORAGE_ACCOUNT_CONNECTION_KEY']

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a local directory to hold blob data
    local_path = "./data"
    today_date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    local_file_name = f"test-{today_date}.txt"
    upload_file_path = os.path.join(local_path, local_file_name)
    
    # Create a unique name for the container
    container_name = "test"
    blob_name = f"retro/{local_file_name}"

    # Create the container
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write("Hello, World!")
    file.close()

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data=data, overwrite=False)

    print("Done")
    
except Exception as ex:
    print('Exception:')
    print(ex)