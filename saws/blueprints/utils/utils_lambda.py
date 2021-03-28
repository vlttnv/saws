import boto3

def get_lambda_info(account):
    client = boto3.client(
        'lambda',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1',
    )

    lambdas = client.list_functions()

    return lambdas
