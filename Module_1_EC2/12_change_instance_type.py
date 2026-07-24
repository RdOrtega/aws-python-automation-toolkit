
import boto3
from botocore.exceptions import ClientError

def change_instance_type(instance_id, new_instance_type, region_name='us-east-1'):
    """
    Safely resizes an EC2 instance (Vertical Scaling).
    Stops the instance, modifies its instance type, and starts it back up.
    """
    ec2_client = boto3.client('ec2', region_name=region_name)

    try:
        print(f"🔄 Starting vertical scaling for instance '{instance_id}' to '{new_instance_type}'...")

        # Step 1: Stop the instance
        print(f"🛑 Stopping instance '{instance_id}'...")
        ec2_client.stop_instances(InstanceIds=[instance_id])
        
        waiter = ec2_client.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])
        print("✅ Instance successfully stopped.")

        # Step 2: Modify Instance Type
        print(f"⚙️ Changing instance type to '{new_instance_type}'...")
        ec2_client.modify_instance_attribute(
            InstanceId=instance_id,
            InstanceType={'Value': new_instance_type}
        )

        # Step 3: Start the instance back up
        print(f"🚀 Starting instance '{instance_id}' with new configuration...")
        ec2_client.start_instances(InstanceIds=[instance_id])
        
        start_waiter = ec2_client.get_waiter('instance_running')
        start_waiter.wait(InstanceIds=[instance_id])
        print(f"🎉 Instance '{instance_id}' is now RUNNING as '{new_instance_type}'!")

    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    INSTANCE_ID = 'i-0123456789abcdef0'
    NEW_TYPE = 't3.small'
    AWS_REGION = 'us-east-1'

    print("⚡ Starting Instance Resize Automation...")
    change_instance_type(INSTANCE_ID, NEW_TYPE, AWS_REGION)
