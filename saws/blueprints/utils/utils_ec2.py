import boto3

# TODO: better client initialization

def get_ec2_info(account):
    client = boto3.client(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    instances = client.describe_instances()

    return instances


def get_key_pairs(account):
    client = boto3.client(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    keys = client.describe_key_pairs()

    return keys


def download_key_pair(account, name):
    client = boto3.client(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    kp = client.create_key_pair(KeyName=name.replace('.pem', ''))

    return kp


def launch_instance(account, props):
    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    result = ec2.create_instances(
        ImageId='ami-0fc970315c2d38f01',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-04926d8b8842fa13e'],
        KeyName='MyIrelandKP',
    )


def stop_instance(account, instance):
    client = boto3.client(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    response = client.stop_instances(InstanceIds=[instance])


def terminate_instance(account, instance):
    client = boto3.client(
        'ec2',
        aws_access_key_id=account.access_key,
        aws_secret_access_key=account.secret_key,
        region_name='eu-west-1'
    )

    response = client.terminate_instances(InstanceIds=[instance])