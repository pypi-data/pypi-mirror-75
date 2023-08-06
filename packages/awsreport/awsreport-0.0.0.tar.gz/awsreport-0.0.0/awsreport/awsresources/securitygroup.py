import boto3
from core.log import Logging

class SgAnalyzer(Logging):
    def __init__(self, sg_rule='0.0.0.0/0'):
        self.ec2 = boto3.client('ec2')
        self.sg_rule = sg_rule

    def find_security_group_by_rule(self):
        security_groups = self.ec2.describe_security_groups()
        for sg in security_groups['SecurityGroups']:
            sg_groupid = sg['GroupId']
            sg_permissions = sg['IpPermissions']

            for permission in sg_permissions:
                if 'ToPort' in permission:
                    to_port = permission['ToPort']

                for ip in permission['IpRanges']:
                    if ip['CidrIp'] == self.sg_rule:
                        self.print_yellow("[+] Security group {0} with inbound rule {1} to port {2}".format(sg_groupid, self.sg_rule, to_port))
