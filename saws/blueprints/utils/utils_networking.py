from saws.blueprints.utils.utils import ec2_client


class SecurityGroup(object):
    def __init__(self, sg, sg_id) -> None:
        self.tcp_ports = []
        self.udp_ports = []
        self.ports = []
        self._id = sg_id
        self.name = sg["GroupName"]
        self.description = sg["Description"]

        for port in sg["IpPermissions"]:
            if port["FromPort"] == port["ToPort"]:
                self.ports.append((port["FromPort"], port["IpProtocol"]))
            else:
                 self.ports.append((f'{port["FromPort"]}-{port["ToPort"]}', port["IpProtocol"]))

    def get_tcp_ports(self):
        str_tcp = str(self.tcp_ports)
        str_tcp = str_tcp.replace("[", "")
        str_tcp = str_tcp.replace("]", "")

        return str_tcp

    def get_udp_ports(self):
        str_udp = str(self.udp_ports)
        str_udp = str_udp.replace("[", "")
        str_udp = str_udp.replace("]", "")

        return str_udp


def get_sgs(account):
    client = ec2_client("eu-west-1", account)
    sgs = client.describe_security_groups()

    return sgs


def create_security_group(account, sg):
    client = ec2_client("eu-west-1", account)

    response = client.create_security_group(
        Description=sg["description"], GroupName=sg["name"]
    )

    return response.get("GroupId")


def delete_security_group(account, sg_id):
    client = ec2_client("eu-west-1", account)

    client.delete_security_group(GroupId=sg_id)


def describe_security_group(account, sg_id):
    client = ec2_client("eu-west-1", account)

    response = client.describe_security_groups(GroupIds=[sg_id])

    if not response["SecurityGroups"]:
        return None
    sg = SecurityGroup(response["SecurityGroups"][0], sg_id=sg_id)
    return sg


def add_sg_port(account, port_from, port_to, protocol, sg_id):
    client = ec2_client("eu-west-1", account)

    ip_permissions = [
        {
            "FromPort": port_from,
            "IpProtocol": protocol,
            "ToPort": port_to,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": "saws",
                },
            ],
        },
    ]

    client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=ip_permissions,
    )


def delete_sg_port(account, port_from, port_to, protocol, sg_id):
    client = ec2_client("eu-west-1", account)

    ip_permissions = [
        {
            "FromPort": port_from,
            "IpProtocol": protocol,
            "ToPort": port_to,
            "IpRanges": [
                {
                    "CidrIp": "0.0.0.0/0",
                    "Description": "saws",
                },
            ],
        },
    ]

    client.revoke_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=ip_permissions,
    )