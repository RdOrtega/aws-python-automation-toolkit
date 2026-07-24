
import boto3
from botocore.exceptions import ClientError

def update_auto_scaling_group(asg_name, min_size, max_size, desired_capacity):
    """
    Updates the capacity limits of an AWS Auto Scaling Group (ASG).
    Useful for scheduled scaling, maintenance windows, or traffic spikes.
    """
    client = boto3.client('autoscaling')
    
    try:
        print(f"🔄 Updating Auto Scaling Group '{asg_name}'...")
        
        response = client.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity
        )
        
        print(f"✅ ASG '{asg_name}' updated successfully!")
        print(f"📊 New Capacity -> Min: {min_size} | Max: {max_size} | Desired: {desired_capacity}")
        return True

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ValidationError':
            print(f"❌ Error: Auto Scaling Group '{asg_name}' not found or invalid parameters.")
        else:
            print(f"❌ AWS API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # ⚠️ Replace with your actual Auto Scaling Group Name in AWS
    ASG_NAME = 'my-production-ec2-asg'
    
    # Target capacity limits
    MIN_SERVERS = 1
    MAX_SERVERS = 5
    DESIRED_SERVERS = 2

    print("🚀 Starting Auto Scaling Group Governance Script...")
    update_auto_scaling_group(ASG_NAME, MIN_SERVERS, MAX_SERVERS, DESIRED_SERVERS)

