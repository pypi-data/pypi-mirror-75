import boto3

from core.log import Logging

class ElasticIpAnalyzer(Logging):
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def find_elastic_dissociated(self):
        elasticips = self.ec2.describe_addresses()

        for ip in elasticips['Addresses']:
            allocation_id = ip['AllocationId']
            public_ip = ip['PublicIp']

            if 'InstanceId' not in ip:
                self.print_yellow("[+] Elastic IP {0} with public IP {1} is not associated".format(allocation_id, public_ip))
