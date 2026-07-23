import boto3
from botocore.exceptions import ClientError

def stop_instances_by_tag(tag_key, tag_value):
    """
    Finds all running EC2 instances with a specific tag and stops them.
    This is a common FinOps practice to save money during non-business hours.
    """
    ec2 = boto3.resource('ec2')
    
    # We filter by the specific Tag AND ensure we only target 'running' instances
    filters = [
        {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]
    
    try:
        print(f"🔍 Searching for RUNNING instances with Tag [{tag_key} : {tag_value}]...")
        instances = list(ec2.instances.filter(Filters=filters))
        
        if not instances:
            print("🤷‍♂️ No matching instances found. Nothing to stop.")
            return

        print(f"🎯 Found {len(instances)} instance(s). Initiating shutdown sequence...")
        
        # Loop through the results and stop them
        for instance in instances:
            print(f"⏸️ Stopping instance {instance.id}...")
            instance.stop()
            
        print("✅ Stop commands sent successfully! Money saved. 💰")
            
    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # Define which tag you want to target for the shutdown.
    # We use the 'Environment=Development' tag we created in our previous script!
    
    TARGET_TAG_KEY = 'Environment'
    TARGET_TAG_VALUE = 'Development'
    
    stop_instances_by_tag(TARGET_TAG_KEY, TARGET_TAG_VALUE)


