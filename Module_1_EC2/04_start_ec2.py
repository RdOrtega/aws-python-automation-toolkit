
import boto3
from botocore.exceptions import ClientError

def start_instances_by_tag(tag_key, tag_value):
    """
    Finds all stopped EC2 instances with a specific tag and starts them.
    Perfect for automating Monday morning server spin-ups.
    """
    ec2 = boto3.resource('ec2')
    
    # Filter by Tag AND ensure we only target 'stopped' instances
    filters = [
        {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ]
    
    try:
        print(f"🔍 Searching for STOPPED instances with Tag [{tag_key} : {tag_value}]...")
        instances = list(ec2.instances.filter(Filters=filters))
        
        if not instances:
            print("🤷‍♂️ No matching stopped instances found. Everything is running!")
            return

        print(f"🚀 Found {len(instances)} instance(s). Initiating boot sequence...")
        
        for instance in instances:
            print(f"▶️ Starting instance {instance.id}...")
            instance.start()
            
        print("✅ Start commands sent successfully! Servers are booting up.")
            
    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    TARGET_TAG_KEY = 'Environment'
    TARGET_TAG_VALUE = 'Development'
    
    print("🌅 Starting Automated EC2 Boot Script...")
    start_instances_by_tag(TARGET_TAG_KEY, TARGET_TAG_VALUE)

