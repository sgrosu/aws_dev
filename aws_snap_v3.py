'''
This program creates snapshots for all tagged volumes in a aws region specified with the --region option

This version is customized for loading credentials from config file
'''

import boto3
import pprint
import datetime
import argparse
import logging
import time
import oreconfig


# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler('/home/sgrosu/' + 'aws_backup_ore.log')
logger_handler.setLevel(logging.INFO)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
# logger.info('Completed configuring logger()!')

logger.info('Started AWS LON backup program at %s', datetime.datetime.now())

argparser = argparse.ArgumentParser(description='Creating snapshots for all EC2 instance tagged volumes in a region')
argparser.add_argument('--region', help='AWS region name')

args = argparser.parse_args()

if not args.region:
    print('You must specify a region')
    exit()

ec2 = boto3.resource('ec2', region_name=args.region, aws_access_key_id=oreconfig.AID, aws_secret_access_key=oreconfig.AKEY)
client = boto3.client('ec2', region_name=args.region, aws_access_key_id=oreconfig.AID,aws_secret_access_key=oreconfig.AKEY)
volumes = ec2.volumes.all()

now = datetime.datetime.now(datetime.timezone.utc)
today = datetime.datetime(now.year, now.month, now.day, tzinfo=datetime.timezone.utc)


volume_ids = []
for vol in volumes:
    if 'OLD' in [item for elem in [list(x.values()) for x in vol.tags] for item in elem]:
        #print(vol.tags[0]['Value'],vol.id)
        volume_ids.append(vol.id)
#print(volume_ids)



for ent in volumes.filter(Filters=[{'Name': 'volume-id', 'Values': volume_ids}]).all():
    #print(ent.tags[0]['Value'])
    snapshot_name = 'BU '+str(datetime.datetime.now().day)+'/' + str(datetime.datetime.now().month)+'/'+str(datetime.datetime.now().year)+' '+ ent.tags[0]['Value']
    #print(snapshot_name)
    snapshot = ec2.create_snapshot(VolumeId=ent.volume_id, Description='created by backup script')
    snapshot.create_tags(Resources=[snapshot.id], Tags=[{'Key': 'Name', 'Value': snapshot_name}])

    # check if snapshot is completed
    snapshot.load()
    while snapshot.state != 'completed':
          time.sleep(10)
          snapshot.load()
    else:
        logger.info("snapshot {} READY".format(snapshot.id))

# adding functionality to delete snapshots older than 1 week, with tags including the word 'BU'


snapshots = client.describe_snapshots()['Snapshots']

#snapshot info

delta = now - datetime.timedelta(days=7)
#print(delta)

for snap in snapshots:

    if snap['Description'] == 'created by backup script' and snap['StartTime'] < delta:
        #print(snap)
        #print(snap['SnapshotId'],snap['Tags'],snap['StartTime'])
        s = client.delete_snapshot(SnapshotId=snap['SnapshotId'])
        logger.info('Deleted snapshot {}'.format(snap['Tags']))

    else:
        logger.info('There are no snapshots to delete')


