
import boto3
from botocore.exceptions import ClientError

def cleanup_unattached_ebs_volumes(ec2_resource):
    """
    Finds and deletes unattached (available) EBS volumes to save costs.
    """
    print("\n🔍 Checking for unattached EBS volumes...")
    try:
        # Filter volumes that are in the 'available' state (not 'in-use')
        unattached_volumes = list(ec2_resource.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        ))
        
        if not unattached_volumes:
            print("✨ No orphaned EBS volumes found.")
            return

        print(f"🗑️ Found {len(unattached_volumes)} unattached volume(s). Cleaning up...")
        for volume in unattached_volumes:
            print(f"   🧨 Deleting Volume ID: {volume.id} (Size: {volume.size} GiB)")
            volume.delete()
        print("✅ Orphaned EBS volumes deleted successfully!")
            
    except ClientError as e:
        print(f"❌ AWS API Error during EBS cleanup: {e}")

def cleanup_unassociated_eips(ec2_client):
    """
    Finds and releases unassociated Elastic IPs (EIPs) to prevent AWS idle charges.
    """
    print("\n🔍 Checking for unassociated Elastic IPs...")
    try:
        # Describe all Elastic IPs in the account
        eips = ec2_client.describe_addresses()['Addresses']
        
        unassociated_eips = [eip for eip in eips if 'InstanceId' not in eip and 'NetworkInterfaceId' not in eip]
        
        if not unassociated_eips:
            print("✨ No orphaned Elastic IPs found.")
            return

        print(f"🗑️ Found {len(unassociated_eips)} unassociated Elastic IP(s). Releasing...")
        for eip in unassociated_eips:
            allocation_id = eip['AllocationId']
            public_ip = eip.get('PublicIp', 'N/A')
            print(f"   💸 Releasing EIP: {public_ip} (AllocationId: {allocation_id})")
            ec2_client.release_address(AllocationId=allocation_id)
        print("✅ Unassociated Elastic IPs released successfully!")
            
    except ClientError as e:
        print(f"❌ AWS API Error during EIP cleanup: {e}")

# ==========================================
# 🚀 AWS LAMBDA ENTRY POINT (PRODUCTION)
# ==========================================
def lambda_handler(event, context):
    print("🧹 Starting AWS Orphaned Resources Sweeper...")
    
    ec2_resource = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')
    
    cleanup_unattached_ebs_volumes(ec2_resource)
    cleanup_unassociated_eips(ec2_client)
    
    print("\n🏁 Cleanup completed successfully.")
    return {
        'statusCode': 200,
        'body': 'Orphaned resources cleanup completed.'
    }

# ==========================================
# 💻 LOCAL EXECUTION ENTRY POINT (TESTING)
# ==========================================
if __name__ == "__main__":
    print("💻 Running cleanup script locally...")
    lambda_handler(None, None)
