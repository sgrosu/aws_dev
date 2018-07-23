
import boto3
from botocore.exceptions import ClientError

import oreconfig

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=oreconfig.AID,
    aws_secret_access_key=oreconfig.AKEY,
    region_name='us-west-2'
)

# dry run start instance

pitcher = 'i-0b5fcac5b8af64938'
ether = 'i-04ed74c10ce499059'

try:
    response = ec2.start_instances(InstanceIds=[pitcher], DryRun=True)
    print(response)
except ClientError as e:
    if 'DryRunOperation' not in str(e):
        raise

try:
    response = ec2.start_instances(InstanceIds=[pitcher], DryRun=False)
    print(response)
except ClientError as e:
    print(e)
