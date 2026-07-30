import boto3
from botocore.exceptions import ClientError

def create_ec2_instance(image_id, instance_type, key_name, tag_name, area, assigned_to):
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
            KeyName=key_name,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': tag_name},
                        {'Key': 'Area', 'Value': area},
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
    KEY_PAIR_NAME = 'your-aws-key-pair-name'
    SERVER_NAME = 'Dev-Web-Server-01'
    Area_Tag = 'Inventory'
    Assigned_To = 'Pedro'
    
    print("🚀 Starting AWS EC2 Provisioning Script...")
    create_ec2_instance(AMI_ID, INSTANCE_TYPE, KEY_PAIR_NAME, SERVER_NAME, Area_Tag, Assigned_To)
  
