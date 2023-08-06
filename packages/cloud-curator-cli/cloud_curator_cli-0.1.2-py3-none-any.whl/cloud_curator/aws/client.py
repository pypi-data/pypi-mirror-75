import boto3


class Client:
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)

    def get_aws_client(self, aws_service):
        return boto3.client(aws_service)