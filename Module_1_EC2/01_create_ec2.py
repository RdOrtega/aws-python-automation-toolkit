import boto3
from botocore.exceptions import ClientError

def create_ec2_instance(image_id, instance_type, tag_name, assigned_to, iam_profile_name):

    # Initialize the high-level Boto3 EC2 Resource
    ec2 = boto3.resource('ec2')
    
    try:
        print(f"🔄 Provisioning a new {instance_type} instance...")
        
        # Provision the EC2 instance with specified configurations
        instances = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            # Attach IAM Role for passwordless web/SSM management (Zero Trust Architecture)
            IamInstanceProfile={
                'Name': iam_profile_name
            },
            # Tag-on-Create strategy for FinOps and governance traceability
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
        
        # Extract the primary created instance object
        instance = instances[0]
        
        # Wait until AWS transitions the instance state from 'pending' to 'running'
        print(f"⏳ Waiting for instance {instance.id} to enter 'running' state...")
        instance.wait_until_running()
        
        # Reload instance properties to fetch newly assigned attributes (e.g., Public IP)
        instance.reload()
        
        print(f"✅ Success! Instance {instance.id} is now RUNNING.")
        
        # Display public IP address if auto-assigned by AWS
        if instance.public_ip_address:
            print(f"🌐 Public IP Address: {instance.public_ip_address}")
            
        return instance.id
        
    except ClientError as e:
        # Catch and handle AWS API exceptions gracefully
        print(f"❌ Error creating instance: {e}")
        return None


if __name__ == "__main__":
    # --- CONFIGURATION PARAMETERS ---
    # Base Ubuntu AMI ID for the target AWS region
    AMI_ID = 'ami-0c7217cdde317cfec'
    
    # Instance type eligible for AWS Free Tier
    INSTANCE_TYPE = 't2.micro'
    
    # Template instance name used as the baseline workstation for clients
    SERVER_NAME = 'AMI_Workspace'
    
    # Administrative owner tag
    ASSIGNED_TO = 'It_Admin'
    
    # Pre-configured IAM Instance Profile granting AmazonSSMManagedInstanceCore access
    IAM_PROFILE = 'SSM-EC2-Role'
    
    print("🚀 Starting AWS EC2 Provisioning Script...")
    
    # Execute the provisioning function
    create_ec2_instance(
        image_id=AMI_ID,
        instance_type=INSTANCE_TYPE,
        tag_name=SERVER_NAME,
        assigned_to=ASSIGNED_TO,
        iam_profile_name=IAM_PROFILE
    )
