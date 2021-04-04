import boto3


class EC2Instance(object):

    image_id = None
    instance_id = None
    instance_type = None
    key_name = None
    launch_time = None
    dns = None
    ip_address = None
    state = None
    security_groups = None
    name = None

    def __init__(self, ec2_json) -> None:
        self.image_id = ec2_json.get('ImageId')
        self.instance_id = ec2_json.get('InstanceId')
        self.instance_type = ec2_json.get('InstanceType')
        self.key_name = ec2_json.get('KeyName')
        self.launch_time = ec2_json.get('LaunchTime')
        self.dns = ec2_json.get('PublicDnsName')
        self.ip_address = ec2_json.get('PublicIpAddress')
        self.state = ec2_json.get('State')
        self.security_groups = ec2_json.get('SecurityGroups')
        for tag in ec2_json.get('Tags', []):
            if tag['Key'] == 'Name':
                self.name = tag['Value']
                break


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

def get_ec2_info(account):
    client = ec2_client('eu-west-1', account)
    instances = client.describe_instances()

    return instances


def get_key_pairs(account):
    client = ec2_client('eu-west-1', account)
    keys = client.describe_key_pairs()

    return keys


def download_key_pair(account, name):
    client = ec2_client('eu-west-1', account)
    kp = client.create_key_pair(KeyName=name.replace('.pem', ''))

    return kp


def launch_instance(account, props):
    resource = ec2_client('eu-west-1', account, _type='resource')
    result = resource.create_instances(
        ImageId='ami-0fc970315c2d38f01',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-04926d8b8842fa13e'],
        KeyName=props['key_name'],
    )


def stop_instance(account, instance):
    client = ec2_client('eu-west-1', account)
    response = client.stop_instances(InstanceIds=[instance])


def terminate_instance(account, instance):
    client = ec2_client('eu-west-1', account)
    response = client.terminate_instances(InstanceIds=[instance])


def describe_instace(account, instance):
    client = ec2_client('eu-west-1', account)
    instance = client.describe_instances(InstanceIds=[instance])

    instance = instance['Reservations'][0]['Instances'][0]

    return instance


def create_tags(account, instance, tags):
    client = ec2_client('eu-west-1', account)
    client.create_tags(Resources=[instance], Tags=tags)