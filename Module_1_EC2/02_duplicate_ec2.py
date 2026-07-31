
import boto3
import time
from botocore.exceptions import ClientError

def get_instance_id_by_name(ec2_client, server_name):
    """
    Helper function: Queries AWS to retrieve the Instance ID matching a specific Name tag.
    """
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [server_name]},
                {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
            ]
        )
        
        # Extract instance IDs from reservation responses
        instances = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
        ]

        if not instances:
            print(f"❌ Error: No active instance found with Name tag '{server_name}'.")
            return None

        found_id = instances[0]
        print(f"🎯 Target server '{server_name}' resolved to Instance ID: {found_id}")
        return found_id

    except ClientError as e:
        print(f"❌ Error querying instance by name: {e}")
        return None


def duplicate_instance(source_server_name, clone_name, assigned_to, iam_profile_name):

    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')

    try:
        # Step 0: Resolve Source Instance ID from Name Tag
        print(f"🔍 Searching for base template server '{source_server_name}'...")
        source_instance_id = get_instance_id_by_name(ec2_client, source_server_name)
        
        if not source_instance_id:
            print("🛑 Execution halted: Source server could not be identified.")
            return None

        # Step 1: Create Amazon Machine Image (AMI) from Source Instance
        print(f"📸 Step 1: Generating AMI from source instance {source_instance_id}...")
        image_response = ec2_client.create_image(
            InstanceId=source_instance_id,
            Name=f"GoldenAMI-{source_server_name}-{int(time.time())}",
            Description="Automated workstation template image created via Python",
            NoReboot=True  # Prevents source server downtime during image creation
        )
        
        image_id = image_response['ImageId']
        print(f"⏳ Waiting for AMI {image_id} to reach 'available' state...")
        
        # Wait until AWS finishes processing the AMI
        waiter = ec2_client.get_waiter('image_available')
        waiter.wait(ImageIds=[image_id])
        print("✅ Golden Image (AMI) is ready!")

        # Step 2: Provision Clone Instance from New AMI
        print("🚀 Step 2: Launching client workstation instance...")
        instances = ec2_resource.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            # Attach IAM Role for passwordless web/SSM management
            IamInstanceProfile={
                'Name': iam_profile_name
            },
            # Assign compliance tags and origin audit trail
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': clone_name},
                        {'Key': 'AssignedTo', 'Value': assigned_to},
                        {'Key': 'ClonedFrom', 'Value': source_server_name}
                    ]
                }
            ]
        )
        
        clone = instances[0]
        print(f"⏳ Waiting for clone instance {clone.id} to enter 'running' state...")
        clone.wait_until_running()
        clone.reload()
        
        print(f"✅ Success! Clone instance {clone.id} is now RUNNING.")
        if clone.public_ip_address:
            print(f"🌐 Clone Public IP: {clone.public_ip_address}")
            
        return clone.id

    except ClientError as e:
        print(f"❌ AWS API Error during duplication: {e}")
        return None


if __name__ == "__main__":
    
    # --- CONFIGURATION PARAMETERS ---
    SOURCE_SERVER_NAME = 'AMI_Workspace'     # Target template instance Name tag created in script 01
    
    # New workstation configuration for onboarded client user
    CLONE_SERVER_NAME = 'Slalom-Workstation-Carlos'
    ASSIGNED_TO = 'Carlos_Luis'
    IAM_PROFILE = 'SSM-EC2-Role'
    
    print("🔄 Starting AWS EC2 Workstation Duplication Workflow...")
    
    # Execute the duplication function
    duplicate_instance(
        source_server_name=SOURCE_SERVER_NAME,
        clone_name=CLONE_SERVER_NAME,
        assigned_to=ASSIGNED_TO,
        iam_profile_name=IAM_PROFILE
    )
    
