import boto3
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from cloud_curator.aws import client

class AccessKeysRotated(object):
    def __init__(self, *args, **kwargs):
        super(AccessKeysRotated, self).__init__(*args, **kwargs)
        self.client = None
        self.aws_client = None
        
        self.key_rotation_period = 90

        self.rotated_by_date = datetime.now(timezone.utc) - timedelta(days=self.key_rotation_period)

    def _get_client(self):
        self.aws_client = client.Client()
        self.client = self.aws_client.get_aws_client('iam')

    def _run_report(self):
        paginator = self.client.get_paginator('list_access_keys')
        response_iterator = paginator.paginate()

        for response in response_iterator:
            for key in response.get('AccessKeyMetadata'):
                if key.get('CreateDate') < self.rotated_by_date:
                    print('old')

    def run(self):
        self._get_client()
        self._run_report()