import boto3

from core.log import Logging

class VolumesAnalyzer(Logging):
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def find_volumes_available(self):
        volumes = self.ec2.describe_volumes()
        for volume in volumes['Volumes']:
            volume_id = volume['VolumeId']
            if not volume['Attachments']:
                self.print_yellow("[+] EBS Volume {0} available".format(volume_id))
