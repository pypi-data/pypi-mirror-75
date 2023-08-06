import boto3

from core.log import Logging
from datetime import datetime, timezone

class IamAnalyzer(Logging):
    def __init__(self, iam_key_age=90):
        self.iam_client = boto3.client('iam')
        self.iam_key_age = iam_key_age
        self.users = list()

    def find_users(self):
        response = self.iam_client.list_users()
        for user in response['Users']:
            self.users.append(user['UserName'])

    def find_max_access_key_age(self):
        self.find_users()

        for user in self.users:
            response = self.iam_client.get_user(UserName=user)
            create_date = response['User']['CreateDate']
            current_date = datetime.now(timezone.utc).replace(microsecond=0)
            verify_date = str(current_date - create_date).split(' ')[0]

            if int(verify_date) > int(self.iam_key_age):
                self.print_yellow("[+] IAM user {0} created more than {1} days ago"\
                        .format(user, verify_date))
