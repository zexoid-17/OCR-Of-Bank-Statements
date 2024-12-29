import os
import boto3
import stat

def fetch_from_s3():
    download_dir = r"C:\Users\DELLL\Downloads\aws_download"  # Specify your preferred download directory

    # Create the download directory if it doesn't exist
    try:
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        os.chmod(download_dir, stat.S_IWRITE)  # Ensure the directory has write permissions
    except Exception as e:
        print(f"Error: Failed to create or modify directory {download_dir}. Details: {e}")
        return

    # Fetch AWS credentials from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        print("Error: Missing AWS credentials. Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as environment variables.")
        return

    # Initialize the S3 client
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="eu-north-1"
        )
    except Exception as e:
        print(f"Error: Failed to initialize S3 client. Details: {e}")
        return

    bucket_name = "infosys-1"
    folder_prefix = "dataset/"

    # Attempt to list and download files from the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                file_key = obj['Key']
                file_name = os.path.basename(file_key)
                download_path = os.path.join(download_dir, file_name)

                if file_name:  # Ensure we only download files, not folder paths
                    print(f"Downloading {file_name}...")
                    try:
                        s3.download_file(bucket_name, file_key, download_path)
                        print(f"{file_name} downloaded successfully to {download_path}.")
                    except Exception as e:
                        print(f"Error: Failed to download {file_name}. Details: {e}")
        else:
            print("No files found in the specified S3 bucket.")
    except Exception as e:
        print(f"Error: Failed to fetch files from S3. Details: {e}")

# Main function to fetch data
def fetch_data():
    print("Fetching data from AWS S3 bucket...")
    fetch_from_s3()
    print("\nData fetch complete.")

# Run the main function
if __name__ == "__main__":
    fetch_data()

