import boto3
from botocore.exceptions import ClientError

def create_ec2_instance(image_id, instance_type, key_name, tag_name):
    """
    Provisions a new EC2 instance, adds tags, and waits for it to be running.
    """
    # Initialize the EC2 resource
    ec2 = boto3.resource('ec2')

    try:
        print(f"🔄 Provisioning a new {instance_type} instance...")
        
        # Create the instance
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
                        {'Key': 'Environment', 'Value': 'Development'}
                    ]
                }
            ]
        )
        
        instance = instances[0]
        
        # Pause the script until the instance is fully running
        print(f"⏳ Waiting for instance {instance.id} to enter 'running' state...")
        instance.wait_until_running()
        
        # Reload the instance attributes to get the dynamically assigned Public IP
        instance.reload()
        
        print(f"✅ Success! Instance {instance.id} is now RUNNING.")
        if instance.public_ip_address:
            print(f"🌐 Public IP Address: {instance.public_ip_address}")
            
        return instance.id
        
    except ClientError as e:
        print(f"❌ Error creating instance: {e}")
        return None

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # Important: Replace these with valid values from your AWS Console before running locally.
    
    # Amazon Linux 2023 AMI (us-east-1 as an example)
    AMI_ID = 'ami-0c7217cdde317cfec' 
    
    # t2.micro is Free Tier eligible
    INSTANCE_TYPE = 't2.micro'
    
    # Must match an existing Key Pair in your AWS EC2 Console
    KEY_PAIR_NAME = 'your-aws-key-pair-name' 
    
    # Tag that will appear in the Name column in AWS
    SERVER_NAME = 'Dev-Web-Server-01'
    
    print("🚀 Starting AWS EC2 Provisioning Script...")
    create_ec2_instance(AMI_ID, INSTANCE_TYPE, KEY_PAIR_NAME, SERVER_NAME)

