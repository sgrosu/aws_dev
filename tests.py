import boto3
import pprint
import config

ec2 = boto3.resource('ec2',
    aws_access_key_id=config.awskey,
    aws_secret_access_key=config.secret,
    region_name='eu-west-2')

def test_modify_tags(inst_id):
    return ec2.create_tags(
        Resources=[inst_id],
        Tags=[
            {
                'Key': 'Oga',
                'Value': 'yes'
            }
        ]
    )


inst = 'i-0cf1bad9aba5fe451'
email = 'i-0202114ca41e7bfed'
print(test_modify_tags(inst))