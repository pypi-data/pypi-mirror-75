import boto3

from core.log import Logging

class IgwAnalyzer(Logging):
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def find_igw_detached(self):
        igws = self.ec2.describe_internet_gateways()

        for igw in igws['InternetGateways']:
            igw_id = igw['InternetGatewayId']
            if not igw['Attachments']:
                self.print_yellow("[+] Internet Gateway {0} it is detached".format(igw_id))
