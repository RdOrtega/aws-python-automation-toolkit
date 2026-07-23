
import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self, region_name='us-east-1'):
        # Initialize the Boto3 client and resource for EC2
        self.ec2 = boto3.client('ec2', region_name=region_name)
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)

    def create_instance(self, ami_id, instance_type="t2.micro", tag_name="DevServer"):
        """Creates a new EC2 instance with a specific Name tag."""
        try:
            print(f"🔄 Creating {instance_type} instance...")
            instances = self.ec2_resource.create_instances(
                ImageId=ami_id,
                MinCount=1,
                MaxCount=1,
                InstanceType=instance_type,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [{'Key': 'Name', 'Value': tag_name}]
                    }
                ]
            )
            instance_id = instances[0].id
            print(f"✅ Instance created successfully! ID: {instance_id}")
            return instance_id
        except ClientError as e:
            print(f"❌ Error creating instance: {e}")

    def list_instances(self):
        """Lists all EC2 instances and their current states."""
        print("\n📊 Current EC2 Instances:")
        try:
            response = self.ec2.describe_instances()
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    state = instance['State']['Name']
                    
                    # Extract the 'Name' tag if it exists
                    name = "Unknown"
                    if 'Tags' in instance:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                                
                    print(f" - ID: {instance_id} | Name: {name} | State: {state}")
        except ClientError as e:
            print(f"❌ Error listing instances: {e}")

    def change_instance_state(self, instance_id, action):
        """Starts, stops, or terminates an instance based on the requested action."""
        try:
            if action == 'start':
                self.ec2.start_instances(InstanceIds=[instance_id])
                print(f"▶️ Starting instance {instance_id}...")
            elif action == 'stop':
                self.ec2.stop_instances(InstanceIds=[instance_id])
                print(f"⏸️ Stopping instance {instance_id}...")
            elif action == 'terminate':
                self.ec2.terminate_instances(InstanceIds=[instance_id])
                print(f"💀 Terminating instance {instance_id}...")
            else:
                print("⚠️ Invalid action. Use 'start', 'stop', or 'terminate'.")
        except ClientError as e:
            print(f"❌ Error changing instance state: {e}")

if __name__ == "__main__":
    # --- EXECUTION TEST ---
    # Ensure AWS CLI is configured ('aws configure') before running this script locally.
    
    manager = EC2Manager(region_name='us-east-1')
    
    # 1. List current instances
    manager.list_instances()
