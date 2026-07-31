import boto3
from botocore.exceptions import ClientError

def create_ec2_instance(image_id, instance_type, tag_name, assigned_to, iam_profile_name):
    """
    Provisions a new EC2 instance, adds tags, and waits for it to be running.
    """
    ec2 = boto3.resource('ec2')
    try:
        print(f"🔄 Provisioning a new {instance_type} instance...")
        
        instances = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            IamInstanceProfile={
                'Name': iam_profile_name
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': tag_name},
                        {'Key': 'AssignedTo', 'Value': assigned_to}
                    ]
                }
            ]
        )
        
        instance = instances[0]
        
        print(f"⏳ Waiting for instance {instance.id} to enter 'running' state...")
        instance.wait_until_running()
        instance.reload()
        
        print(f"✅ Success! Instance {instance.id} is now RUNNING.")
        if instance.public_ip_address:
            print(f"🌐 Public IP Address: {instance.public_ip_address}")
            
        return instance.id
        
    except ClientError as e:
        print(f"❌ Error creating instance: {e}")
        return None


if __name__ == "__main__":
    AMI_ID = 'ami-0c7217cdde317cfec'
    INSTANCE_TYPE = 't2.micro'
    SERVER_NAME = 'Dev-Tech-AppServer-01'
    Assigned_To = 'Pedro'
    IAM_PROFILE = 'SSM-EC2-Role'  # el nombre del Instance Profile que creaste en IAM
    
    print("🚀 Starting AWS EC2 Provisioning Script...")
    create_ec2_instance(AMI_ID, INSTANCE_TYPE, SERVER_NAME, Assigned_To, IAM_PROFILE)
  
