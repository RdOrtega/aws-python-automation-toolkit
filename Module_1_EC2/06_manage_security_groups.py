
import boto3
from botocore.exceptions import ClientError

def create_and_configure_sg(group_name, description):
    """
    Creates a new EC2 Security Group and opens essential ports (SSH and HTTP).
    """
    # For Security Groups, using the 'client' interface is usually more direct
    ec2_client = boto3.client('ec2')
    
    try:
        print(f"🛡️ Creating Security Group '{group_name}'...")
        
        # Step 1: Create the empty security group
        response = ec2_client.create_security_group(
            GroupName=group_name, 
            Description=description
        )
            
        security_group_id = response['GroupId']
        print(f"✅ Security Group created successfully! ID: {security_group_id}")
        
        print("🔓 Configuring firewall rules (Opening ports 22 and 80)...")
        
        # Step 2: Add Inbound (Ingress) Rules
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Allow SSH access for admins'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Allow HTTP web traffic for users'}]
                }
            ]
        )
        
        print("✅ Firewall rules updated successfully!")
        return security_group_id
        
    except ClientError as e:
        # PRO TIP: We catch the specific error if the group name is already taken!
        if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            print(f"⚠️ Warning: A Security Group named '{group_name}' already exists in this account.")
        else:
            print(f"❌ AWS API Error: {e}")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    SG_NAME = 'Web-Tier-Firewall'
    SG_DESCRIPTION = 'Automated security group allowing SSH and HTTP traffic'
    
    print("🧱 Starting Security Group Manager Script...")
    create_and_configure_sg(SG_NAME, SG_DESCRIPTION)

