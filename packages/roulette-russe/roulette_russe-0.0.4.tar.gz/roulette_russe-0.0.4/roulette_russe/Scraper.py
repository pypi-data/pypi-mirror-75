import vaex
import boto3
from botocore.exceptions import ClientError
from abc import abstractmethod
import logging


class Scraper(object):
    def __init__(self, input_config: dict, output_columns: list, roulette_russe=None):
        output_dict = dict()
        for i in range(len(output_columns)):
            output_dict[output_columns[i]] = []
        self.output_dataset = vaex.from_dict(output_dict)
        self.input_config = input_config
        self.roulette_russe = roulette_russe
        print(self.output_dataset)

    @abstractmethod
    def scrap(self):
        pass

    def to_csv(self, path):
        self.output_dataset.export_csv(path=path)

    def to_parquet(self, path):
        self.output_dataset.export_parquet(path=path)

    @abstractmethod
    def quality_check(self):
        pass

    def to_s3(self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str, file_name: str):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client('s3')
        self.to_parquet(file_name)
        try:
            s3.upload_file(file_name, bucket_name, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True


d = ['OK1', 'OK2', 'OK3']
s = Scraper({}, d)
