import boto3

def ec2_client(region, account, _type='client'):
    if _type == 'client':
        client = boto3.client(
            'ec2',
            aws_access_key_id=account.access_key,
            aws_secret_access_key=account.secret_key,
            region_name=region,
        )

        return client
    elif _type == 'resource':
        resource = boto3.resource(
            'ec2',
            aws_access_key_id=account.access_key,
            aws_secret_access_key=account.secret_key,
            region_name=region,
        )

        return resource