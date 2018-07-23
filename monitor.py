import boto3
import config
import pprint
import datetime
import time

client = boto3.client(
    'cloudwatch',
    aws_access_key_id=config.aws,
    aws_secret_access_key=config.sec,
    region_name='eu-west-2'
)


#print(dir(client))

stats = client.get_metric_statistics(Period=1,
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
    EndTime=datetime.datetime.utcnow(),
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Statistics=['Average'],
    Dimensions=[{'Name':'InstanceId', 'Value':'i-045114c528113be81'}]
)

for i in range(10):
    pprint.pprint(stats['Datapoints'][0]['Average'])
    time.sleep(10)

