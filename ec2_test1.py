import boto3

ec2_obj = boto3.client('ec2')
ec2_out = ec2_obj.describe_instances(Filters=[{
	'Name': 'tag:StudentID',
	'Values': ['00']
}])

for inst_list in ec2_out['Reservations']:
	for inst in inst_list['Instances']:
		print(inst['InstanceId'])
