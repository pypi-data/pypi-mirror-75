from awsresources.ami import AmiAnalyzer
from awsresources.securitygroup import SgAnalyzer
from awsresources.elasticip import ElasticIpAnalyzer
from awsresources.iam import IamAnalyzer
from awsresources.igw import IgwAnalyzer
from awsresources.s3 import S3Analyzer
from awsresources.volumes import VolumesAnalyzer

from core.argument_parser import CliArgumentParser
from core.log import Logging

class Analyzer(Logging):
    def __init__(self):
        self.log = Logging()

    def aws_scan(self, args):
        if args.ami and args.owner:
            return AmiAnalyzer().find_public_ami(owners=[args.owner])

        if args.sg:
            if args.cidr:
                return SgAnalyzer(args.cidr).find_security_group_by_rule()

            return SgAnalyzer().find_security_group_by_rule()

        if args.elasticip:
            return ElasticIpAnalyzer().find_elastic_dissociated()

        if args.iam:
            if args.iam_max_age:
                return IamAnalyzer(args.iam_max_age).find_max_access_key_age()

            return IamAnalyzer().find_max_access_key_age()

        if args.igw:
            return IgwAnalyzer().find_igw_detached()

        if args.s3:
            return S3Analyzer().find_buckets_public()

        if args.volumes:
            return VolumesAnalyzer().find_volumes_available()
