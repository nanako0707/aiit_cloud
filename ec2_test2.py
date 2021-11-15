import boto3

ec2 = boto3.resource('ec2')
inst_list = ec2.instances.filter(
	Filters=[{
		'Name': 'tag:StudentID',
		'Values': ['00']
	}]
)

for inst in inst_list:
	instance_id = inst.instance_id
	instance_type = inst.instance_type
	print(instance_id, instance_type)
	#response = instance.start()
	#response = instance.stop(Force=True)
