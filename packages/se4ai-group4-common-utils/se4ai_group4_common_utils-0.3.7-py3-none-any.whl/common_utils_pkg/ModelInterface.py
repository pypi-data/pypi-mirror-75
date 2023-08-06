import os
import boto3
from surprise import dump
from common_utils_pkg.Model import Model

class ModelInterface:
    def __init__(self, bucket_name='se4ai-group-4-aws', aws_key=None, aws_secret=None):
        self.s3_client = boto3.client('s3',aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)
        self.bucket_name = bucket_name 

    def download_model(self, model_name):
        # TODO: we can introduce versioning to S3 here
        temp_model_path = 'tmp_model'
        self.s3_client.download_file(self.bucket_name, model_name, temp_model_path)
        predictions, algo = dump.load(file_name=temp_model_path)
        os.remove(temp_model_path)
        return Model(algo)

    def save_model(self, model_name, model):
        temp_model_path = 'tmp_model'
        dump.dump(file_name=temp_model_path, predictions=None, algo=model)
        self.s3_client.upload_file(temp_model_path, self.bucket_name, model_name)
        os.remove(temp_model_path)