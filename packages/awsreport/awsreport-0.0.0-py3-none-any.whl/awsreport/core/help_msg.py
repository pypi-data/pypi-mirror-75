help_msg = '''
aws_report.py [OPTIONS]

Options:
  --s3          Search buckets public in s3
  --iam         Search iam users based on creation date
  --iam-max-age Use max-age to search for users created more than X days ago
  --sg          Search security groups with inbound specific rule
  --elasticip   Search elastic IP not associated
  --volumes     Search volumes available
  --ami         Search AMIs with permission public
  --owner       Defines the owner of the resources to be found
  --igw         Search internet gateways detached
  --help        Show this message and exit.

Examples:
    python awsreport.py --s3
    python awsreport.py --iam --owner 296192063842
    python awsreport.py --iam --iam-max-age 60
    python awsreport.py --sg --cidr 192.168.1.0/24 or
    python awsreport.py --sg (cidr default is 0.0.0.0)
'''
