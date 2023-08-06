import boto3

from collections import defaultdict
from core.log import Logging

class S3Analyzer(Logging):
    def __init__(self):
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

        self.groups = {
            "http://acs.amazonaws.com/groups/global/AllUsers": "Everyone",
            "http://acs.amazonaws.com/groups/global/AuthenticatedUsers": "Authenticated AWS users"
        }

    def find_buckets_public(self):
        buckets = self.s3_resource.buckets.all()

        for bucket in buckets:
            acl = bucket.Acl()
            public, grants = self.verify_acl(acl)

            if public:
                self.print_yellow("[+] Bucket {0} is public!".format(bucket.name))

    def verify_acl(self, acl):
        dangerous = defaultdict(list)

        for grant in acl.grants:
            grantee = grant["Grantee"]
            if grantee["Type"] == "Group" and grantee["URI"] in self.groups:
                dangerous[grantee["URI"]].append(grant["Permission"])

        if dangerous:
            public = True
        else:
            public = False

        return public, dangerous
