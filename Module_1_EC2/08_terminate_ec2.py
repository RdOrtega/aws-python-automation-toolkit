
import boto3
from botocore.exceptions import ClientError

def terminate_ec2_instance(instance_id):
    """
    Permanently terminates an EC2 instance.
    WARNING: This action cannot be undone. All ephemeral and root volume data will be lost.
    """
    ec2 = boto3.resource('ec2')
    
    try:
        instance = ec2.Instance(instance_id)
        
        # Check current state before attempting to terminate
        state = instance.state['Name']
        if state == 'terminated':
            print(f"⚠️ Instance {instance_id} is already terminated.")
            return

        print(f"🧨 WARNING: Initiating termination sequence for {instance_id}...")
        instance.terminate()
        
        # Pause script until AWS confirms the instance is fully destroyed
        print(f"⏳ Waiting for instance {instance_id} to be fully destroyed (this may take a minute)...")
        instance.wait_until_terminated()
        
        print("✅ Termination complete! The server is destroyed and you will no longer be billed for it.")
        
    except ClientError as e:
        if 'InvalidInstanceID.NotFound' in str(e):
            print(f"❌ Error: Instance {instance_id} does not exist.")
        else:
            print(f"❌ AWS API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # ⚠️ DANGER ZONE: Put the Instance ID you want to permanently delete.
    TARGET_INSTANCE_ID = 'i-0123456789abcdef0' 
    
    print("🗑️ Starting EC2 Termination Script...")
    terminate_ec2_instance(TARGET_INSTANCE_ID)

