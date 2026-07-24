
import boto3
import time
from botocore.exceptions import ClientError

def duplicate_instance(source_instance_id, clone_name):
    """
    Creates an Amazon Machine Image (AMI) from an existing instance 
    and launches a new cloned instance from that image.
    """
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')

    try:
        # Step 1: Create the Image (AMI)
        print(f"📸 Step 1: Creating AMI from instance {source_instance_id}...")
        image_response = ec2_client.create_image(
            InstanceId=source_instance_id,
            Name=f"Backup-{source_instance_id}-{int(time.time())}",
            Description="Automated clone image created via Python",
            NoReboot=True  # PRO TIP: This prevents the source server from shutting down during backup
        )
        
        image_id = image_response['ImageId']
        print(f"⏳ Waiting for AMI {image_id} to be available (this takes a few minutes)...")
        
        # Pause script until AWS finishes processing the image
        waiter = ec2_client.get_waiter('image_available')
        waiter.wait(ImageIds=[image_id])
        print("✅ AMI is ready!")

        # Step 2: Launch the Clone
        print("🚀 Step 2: Launching clone instance...")
        instances = ec2_resource.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': clone_name},
                        {'Key': 'Environment', 'Value': 'Development'},
                        {'Key': 'ClonedFrom', 'Value': source_instance_id}
                    ]
                }
            ]
        )
        
        clone = instances[0]
        print(f"⏳ Waiting for clone instance {clone.id} to be running...")
        clone.wait_until_running()
        clone.reload()
        
        print(f"✅ Success! Clone {clone.id} is RUNNING.")
        if clone.public_ip_address:
            print(f"🌐 Clone Public IP: {clone.public_ip_address}")
            
        return clone.id

    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
        return None

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # Put the Instance ID of the server you created in script 01 here:
    SOURCE_INSTANCE_ID = 'i-0123456789abcdef0' 
    CLONE_SERVER_NAME = 'Dev-Web-Server-Clone'
    
    print("🔄 Starting EC2 Duplication Script...")
    duplicate_instance(SOURCE_INSTANCE_ID, CLONE_SERVER_NAME)
