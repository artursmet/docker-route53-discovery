"""
Script updates selected record to EC2 local ip address
"""

import os

import boto3
import requests

ASSUME_ROLE_ARN = os.getenv('ASSUME_ROLE_ARN')
ROLE_SESSION_NAME = os.getenv('ROLE_SESSION_NAME')
ROUTE53_ZONE_ID = os.getenv('DNS_ZONE_ID')
DNS_RECORD_NAME = os.getenv('DNS_RECORD_NAME')

def get_route53_client(role_arn=None, role_session_name=None):
    if role_arn and role_session_name:
        session = role_arn_to_session(role_arn, role_session_name)
        return session.client('route53')
    return boto3.client('route53')

def get_ec2_local_ip():
    data = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4")
    return data.text

def role_arn_to_session(role_arn, role_session_name):
    """
    Usage :
        session = role_arn_to_session(
            RoleArn='arn:aws:iam::012345678901:role/example-role',
            RoleSessionName='ExampleSessionName')
        client = session.client('sqs')
    Credits: https://gist.github.com/gene1wood/938ff578fbe57cf894a105b4107702de
    """
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=role_arn, RoleSessionName=role_session_name)

    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])


def update_record(record_name, value):
    route_53 = get_route53_client(ASSUME_ROLE_ARN, ROLE_SESSION_NAME)
    route_53.change_resource_record_sets(
        HostedZoneId=ROUTE53_ZONE_ID,
        ChangeBatch={
           'Changes': [
            {'Action': 'UPSERT',
             'ResourceRecordSet': {
                'Name': record_name,
                'Type': 'A',
                'TTL': 30,
                'ResourceRecords': [{'Value': value}]
            }}]
        }
    )

if __name__ == '__main__':
    local_ip = get_ec2_local_ip()
    update_record(DNS_RECORD_NAME, local_ip)
