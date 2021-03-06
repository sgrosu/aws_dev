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


ami_id = 'ami-d4da38b3'
maxcount = 5
inst_type = 't2.medium'
sec_group = ['sg-48562b21']
subnet = 'subnet-55f93e18'
tag = {"Key": "Purpose", "Value": "Compute"}

#print(create_instances(ami_id,maxcount,inst_type,sec_group,subnet,tag))
terminate_instances(['i-03032a9ea3204368c', 'i-06b57f3f239fa4417', 'i-05afe9e70d1ab0f48', 'i-02234bddc03f147f7', 'i-0a295100d441c22a3'])

#print(config.awskey)