
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

def backup_ebs_volumes(tag_key, tag_value):
    """
    Finds all EC2 instances with a specific tag and creates snapshots 
    (backups) of their attached EBS volumes.
    """
    ec2 = boto3.resource('ec2')
    
    # Filter instances that need backing up
    filters = [{'Name': f'tag:{tag_key}', 'Values': [tag_value]}]
    
    try:
        print(f"🔍 Searching for instances to backup (Tag: [{tag_key} : {tag_value}])...")
        instances = list(ec2.instances.filter(Filters=filters))
        
        if not instances:
            print("🤷‍♂️ No instances found for backup.")
            return

        for instance in instances:
            print(f"📦 Processing Instance: {instance.id}")
            
            # An instance can have multiple hard drives (Volumes), we iterate through all of them
            for volume in instance.volumes.all():
                
                # 🕒 The time trick is perfect here for unique backup names!
                timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
                desc = f"Auto-backup for {instance.id} - Vol {volume.id} on {timestamp}"
                
                print(f"   📸 Snapshotting Volume: {volume.id}...")
                snapshot = volume.create_snapshot(
                    Description=desc,
                    TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': [
                                {'Key': 'Name', 'Value': f"Backup-{instance.id}-{timestamp}"},
                                {'Key': 'OriginalVolume', 'Value': volume.id},
                                {'Key': 'CreatedBy', 'Value': 'Python-Automation'}
                            ]
                        }
                    ]
                )
                print(f"   ✅ Snapshot started: {snapshot.id}")
                
        print("🎉 All backup jobs successfully initiated!")
            
    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    TARGET_TAG_KEY = 'Environment'
    TARGET_TAG_VALUE = 'Development'
    
    print("💾 Starting Automated EBS Backup Script...")
    backup_ebs_volumes(TARGET_TAG_KEY, TARGET_TAG_VALUE)

