import boto3
import config
import pprint

ec2_client = boto3.client('ec2',region_name='eu-west-2',aws_access_key_id=config.awskey,aws_secret_access_key=config.secret)

#response = ec2_client.start_instances(InstanceIds=['i-0cf1bad9aba5fe451'], DryRun=True)
#response = ec2_client.stop_instances(InstanceIds=['i-00459f07ad5e95361'], DryRun=True)
response = ec2_client.terminate_instances(InstanceIds=['i-00459f07ad5e95361'], DryRun=True)

pprint(response) # will display error if DryRun is set to False -  but will actually perform the operation