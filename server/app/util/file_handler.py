import os
from werkzeug.utils import secure_filename
import boto3


class FileHandler:
    def save(self, file, filename):
        pass

    def read(self, filename):
        pass


class FileSystemFileHandler(FileHandler):
    def __init__(self, upload_path):
        self.upload_path = upload_path

    def save(self, file, filename):
        if file:
            new_file_name = secure_filename(filename)
            file.save(os.path.join(self.upload_path, new_file_name))
        else:
            raise FileNotFoundError()

    def read(self, filename):
        file_path = f"{self.upload_path}/{filename}"
        if os.path.exists(file_path):
            return open(file_path, "rb")

        return None


class AWSFileHandler(FileHandler):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def save(self, file, filename):
        self.s3_client.upload_file(file, self.bucket_name, filename)

    def read(self, filename):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
        return response['Body'].read()
