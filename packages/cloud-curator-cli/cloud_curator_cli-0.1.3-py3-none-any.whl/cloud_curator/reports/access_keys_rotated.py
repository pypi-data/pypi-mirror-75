import boto3
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import csv
from cloud_curator.aws import client

class AccessKeysRotated(object):
    def __init__(self, *args, **kwargs):
        super(AccessKeysRotated, self).__init__(*args, **kwargs)
        self.client = None
        self.aws_client = None
        
        self.key_rotation_period = 10

        self.earlist_date = datetime.now(timezone.utc) - timedelta(days=self.key_rotation_period)

        self.list_of_keys = []

    def get_client(self):
        self.aws_client = client.Client()
        self.client = self.aws_client.get_aws_client('iam')

    def run_report(self):
        print("reporting")
        paginator = self.client.get_paginator('list_access_keys')
        response_iterator = paginator.paginate()

        for response in response_iterator:
            for key in response.get('AccessKeyMetadata'):
                if key.get('CreateDate') < self.earlist_date:
                    self.list_of_keys.append(key)

    def create_report(self):
        keys = self.list_of_keys[0].keys()
        
        with open('AccessKeysRotated.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.list_of_keys)

    def run(self):
        self.get_client()
        self.run_report()
        self.create_report()