

import boto3
import time
from botocore.exceptions import ClientError

def create_custom_ami(source_server_name, custom_ami_name):
    """
    Finds a source EC2 by Name tag and generates a custom Golden AMI.
    """
    ec2_client = boto3.client('ec2')
    
    try:
        # Step 1: Find server ID by Name tag
        print(f"🔍 Locating source server '{source_server_name}'...")
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [source_server_name]},
                {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
            ]
        )
        reservations = response.get('Reservations', [])
        if not reservations or not reservations[0]['Instances']:
            print(f"❌ Server '{source_server_name}' not found.")
            return None
            
        source_id = reservations[0]['Instances'][0]['InstanceId']
        
        # Step 2: Create image
        print(f"📸 Creating AMI '{custom_ami_name}' from instance {source_id}...")
        img_response = ec2_client.create_image(
            InstanceId=source_id,
            Name=custom_ami_name,
            Description="Custom Golden AMI for client workstations",
            NoReboot=True
        )
        
        new_ami_id = img_response['ImageId']
        print(f"⏳ Waiting for AMI {new_ami_id} to be available...")
        
        waiter = ec2_client.get_waiter('image_available')
        waiter.wait(ImageIds=[new_ami_id])
        
        print(f"✅ AMI Created Successfully! ID: {new_ami_id}")
        return new_ami_id
        
    except ClientError as e:
        print(f"❌ Error creating AMI: {e}")
        return None


if __name__ == "__main__":
    SOURCE_SERVER = 'AMI_Workspace'
    # Distinguishable name with timestamp
    AMI_NAME = f"GoldenAMI-Slalom-v1-{int(time.time())}"
    
    create_custom_ami(
        source_server_name=SOURCE_SERVER,
        custom_ami_name=AMI_NAME
    )
