import os
from abc import ABC, abstractmethod
from io import BytesIO
from werkzeug.utils import secure_filename
import boto3


class FileHandler(ABC):
    @abstractmethod
    def save(self, file, filename):
        pass

    @abstractmethod
    def read(self, filename):
        pass

    @abstractmethod
    def file_exists(self, filename):
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

    def file_exists(self, filename):
        return os.path.exists(f"{self.upload_path}/{filename}")

    def read(self, filename):
        file_path = f"{self.upload_path}/{filename}"
        if os.path.exists(file_path):
            return open(file_path, "rb")

        return None


class AWSFileHandler(FileHandler):
    def __init__(self, bucket_name, upload_path):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")
        self.upload_path = upload_path

    def save(self, file, filename):
        self.s3_client.upload_fileobj(
            file, self.bucket_name, f"{self.upload_path}/{filename}"
        )

    def file_exists(self, filename):
        results = self.s3_client.list_objects(
            Bucket=self.bucket_name, Prefix=f"{self.upload_path}/{filename}"
        )
        return "Contents" in results

    def read(self, filename):
        response = self.s3_client.get_object(
            Bucket=self.bucket_name, Key=f"{self.upload_path}/{filename}"
        )
        return BytesIO(response["Body"].read())
