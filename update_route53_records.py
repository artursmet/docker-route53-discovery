"""
Script updates selected record to EC2 local ip address
"""

import os

import boto3
import requests

ROUTE53_ZONE_ID = os.getenv('DNS_ZONE_ID')
DNS_RECORD_NAME = os.getenv('DNS_RECORD_NAME')

route_53 = boto3.client('route53')

def get_ec2_local_ip():
    data = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4")
    return data.content

def update_record(record_name, value):
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
