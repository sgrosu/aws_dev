import boto3
import pprint
import config

ec2 = boto3.resource('ec2',
    aws_access_key_id=config.awskey,
    aws_secret_access_key=config.secret,
    region_name='eu-west-2')


def create_instances(ami,maxcount,inst_type,sec_group,subnet,tag):
    instances = ec2.create_instances(
        ImageId=ami,
        MinCount=1,
        MaxCount=maxcount,
        InstanceType=inst_type,
        SecurityGroupIds=sec_group,
        SubnetId=subnet,
        TagSpecifications=[{'ResourceType': 'instance','Tags': [tag]}]
        )
    ids = [inst.id for inst in instances]
    return ids

def terminate_instances(inst):
    ec2.instances.filter(InstanceIds=inst).terminate()
    return 'Terminated instances' + str(inst)

#inst_to_terminate = create_instances(ami_id,maxcount,inst_type,sec_group,subnet,tag)


ami_id = 'ami-dff017b8'
maxcount = 3
inst_type = 't2.micro'
sec_group = ['sg-48562b21']
subnet = 'subnet-b608a7cd'
tag = {"Key": "Purpose", "Value": "Compute"}

#print(create_instances(ami_id,maxcount,inst_type,sec_group,subnet,tag))
#terminate_instances(['i-025e3025f2f7bf320', 'i-0a6b471c392a1727d', 'i-04e262e457c384892'])

#print(config.awskey)