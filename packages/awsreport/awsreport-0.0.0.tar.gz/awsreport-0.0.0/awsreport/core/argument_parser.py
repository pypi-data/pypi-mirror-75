import argparse

from core.help_msg import help_msg

class CliArgumentParser():
    def argument_parser(self):
        parser = argparse.ArgumentParser(add_help=False, usage=help_msg)

        parser.add_argument('--ami', '--images',
                            action="store_true",
                            required=False)

        parser.add_argument('--sg', '--securitygroup',
                            action="store_true",
                            required=False)

        parser.add_argument('--cidr',
                            required=False)

        parser.add_argument('--owner', '--imagesowner',
                            required=False)

        parser.add_argument('--elasticip',
                            action="store_true",
                            required=False)

        parser.add_argument('--iam',
                            action="store_true",
                            required=False)

        parser.add_argument('--iam-max-age',
                            required=False)

        parser.add_argument('--igw',
                            action="store_true",
                            required=False)

        parser.add_argument('--s3',
                            action="store_true",
                            required=False)

        parser.add_argument('--volumes',
                            action="store_true",
                            required=False)

        args = parser.parse_args()

        return args
