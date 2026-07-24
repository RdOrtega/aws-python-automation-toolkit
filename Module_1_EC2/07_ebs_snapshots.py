import boto3
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError

# --- CONFIGURATION VARIABLES ---
TARGET_TAG_KEY = 'Area'
TARGET_TAG_VALUES = ['Contabilidad', 'Ventas', 'RecursosHumanos', 'Sistemas']
RETENTION_DAYS = 30  # Snapshots older than this will be destroyed

def backup_ebs_volumes():
    """
    Finds targeted EC2 instances and backups their attached EBS volumes.
    """
    ec2 = boto3.resource('ec2')
    filters = [{'Name': f'tag:{TARGET_TAG_KEY}', 'Values': TARGET_TAG_VALUES}]
    
    try:
        print(f"🔍 [BACKUP] Searching for instances (Tag: [{TARGET_TAG_KEY} : {TARGET_TAG_VALUES}])...")
        instances = list(ec2.instances.filter(Filters=filters))
        
        if not instances:
            print("🤷‍♂️ [BACKUP] No instances found for backup.")
            return

        for instance in instances:
            for volume in instance.volumes.all():
                timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
                desc = f"Auto-backup for {instance.id} - Vol {volume.id} on {timestamp}"
                
                print(f"   📸 Snapshotting Volume: {volume.id}...")
                volume.create_snapshot(
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
        print("✅ [BACKUP] All backup jobs successfully initiated!")
            
    except Exception as e:
        print(f"❌ [BACKUP] Error: {e}")

def cleanup_old_snapshots():
    """
    Finds snapshots created by this script and deletes those older than RETENTION_DAYS.
    """
    ec2_client = boto3.client('ec2')
    
    # Calculate the exact cutoff date (UTC timezone to match AWS)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    print(f"🧹 [CLEANUP] Deleting automated snapshots older than {RETENTION_DAYS} days ({cutoff_date.strftime('%Y-%m-%d')})...")
    
    try:
        # Filter ONLY snapshots created by our automation to avoid deleting manual backups
        snapshots = ec2_client.describe_snapshots(
            OwnerIds=['self'],
            Filters=[{'Name': 'tag:CreatedBy', 'Values': ['Python-Automation']}]
        )['Snapshots']
        
        deleted_count = 0
        for snap in snapshots:
            snap_date = snap['StartTime']
            
            if snap_date < cutoff_date:
                print(f"   🧨 Deleting old snapshot {snap['SnapshotId']} (Created: {snap_date.strftime('%Y-%m-%d')})")
                ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
                deleted_count += 1
                
        if deleted_count == 0:
            print("✨ [CLEANUP] No old snapshots needed deleting today.")
        else:
            print(f"✅ [CLEANUP] Successfully deleted {deleted_count} old snapshot(s). Money saved! 💰")
            
    except Exception as e:
        print(f"❌ [CLEANUP] Error: {e}")

# ==========================================
# 🚀 AWS LAMBDA ENTRY POINT (PRODUCTION)
# ==========================================
def lambda_handler(event, context):
    """
    This is the function AWS Lambda will trigger automatically (e.g., via EventBridge cron).
    """
    print("⏰ Lambda execution started.")
    backup_ebs_volumes()
    cleanup_old_snapshots()
    print("🏁 Lambda execution finished.")
    return {
        'statusCode': 200,
        'body': 'Backup and cleanup completed successfully.'
    }

# ==========================================
# 💻 LOCAL EXECUTION ENTRY POINT (TESTING)
# ==========================================
if __name__ == "__main__":
    print("💻 Running script locally (Simulating Lambda)...")
    # We call the lambda_handler manually, passing 'None' since we don't have AWS events here
    lambda_handler(None, None)

