import config_admin
import boto3

client = boto3.client(
    'iam',
    aws_access_key_id=config_admin.awskey,
    aws_secret_access_key=config_admin.secret,
    region_name='eu-west-2'
)

principals_to_check = ['arn:aws:iam::994667631481:user/ComputeAdmin']

actions_to_check = ['iam:AddRolesToInstanceProfile',
                    'ec2:DescribeInstances']

with open('createpol.txt') as policy_file:
    policy = policy_file.read()

for principal in principals_to_check:
    simulationdict = client.simulate_principal_policy(
        PolicySourceArn = principal, ActionNames = actions_to_check,
        PolicyInputList = [policy]
    )
    evalresults = simulationdict['EvaluationResults']
    for evalresult in evalresults:
        evaldecision = evalresult['EvalDecision']
        if (evaldecision == 'allowed'):
            print('Found an allowed action - more work!' + str(evalresult))