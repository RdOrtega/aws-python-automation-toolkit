
import boto3
from botocore.exceptions import ClientError

def generate_ec2_health_report(target_regions):
    """
    Audits EC2 instances across one or multiple specified AWS regions.
    
    :param target_regions: List of region names (e.g., ['us-east-1', 'us-west-2'])
    """
    if isinstance(target_regions, str):
        target_regions = [target_regions]

    for region in target_regions:
        print(f"\n==================================================================")
        print(f"🔍 AUDITING REGION: [{region.upper()}]")
        print(f"==================================================================")

        try:
            ec2_client = boto3.client('ec2', region_name=region)
            response = ec2_client.describe_instance_status(IncludeAllInstances=True)
            statuses = response.get('InstanceStatuses', [])

            if not statuses:
                print(f"ℹ️ No EC2 instances found in region '{region}'.")
                continue

            print(f"{'Instance ID':<20} | {'State':<12} | {'System Check':<15} | {'Instance Check':<15}")
            print("-" * 70)

            for status in statuses:
                instance_id = status['InstanceId']
                state = status['InstanceState']['Name']
                
                system_check = status['SystemStatus']['Status'].upper()
                instance_check = status['InstanceStatus']['Status'].upper()

                system_fmt = f"✅ {system_check}" if system_check == 'OK' else f"⚠️ {system_check}"
                instance_fmt = f"✅ {instance_check}" if instance_check == 'OK' else f"⚠️ {instance_check}"
                
                if state != 'running':
                    system_fmt = "➖ N/A (Stopped)"
                    instance_fmt = "➖ N/A (Stopped)"

                print(f"{instance_id:<20} | {state:<12} | {system_fmt:<15} | {instance_fmt:<15}")

            print("-" * 70)

        except ClientError as e:
            print(f"❌ AWS API Error in region '{region}': {e}")
        except Exception as e:
            print(f"❌ Unexpected error in region '{region}': {e}")

    print("\n🎉 Multi-Region Audit Completed!")

if __name__ == "__main__":
    # --- CONFIGURATION VARIABLES ---
    # Option 1: Audit a single region
    # TARGET_REGIONS = ['us-east-1']
    
    # Option 2: Audit multiple regions in one execution
    TARGET_REGIONS = ['us-east-1', 'us-west-2', 'eu-west-1']

    generate_ec2_health_report(TARGET_REGIONS)

