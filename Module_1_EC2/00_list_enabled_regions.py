
import boto3
from botocore.exceptions import ClientError

def get_enabled_aws_regions():
    """
    Queries AWS EC2 global endpoint to list all currently enabled regions for this account.
    """
    # EC2 endpoint in us-east-1 is used to query global region availability
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    try:
        print("🌐 Querying AWS for enabled regions in your account...\n")
        
        # 'AllRegions=False' filters only regions enabled for your AWS account
        response = ec2_client.describe_regions(AllRegions=False)
        regions = response.get('Regions', [])

        print(f"✅ Found {len(regions)} enabled regions:\n")
        print(f"{'Region Name':<20} | {'Endpoint Status'}")
        print("-" * 45)

        region_names = []
        for reg in regions:
            name = reg['RegionName']
            opt_in_status = reg.get('OptInStatus', 'opt-in-not-required')
            region_names.append(name)
            print(f"{name:<20} | {opt_in_status}")

        print("-" * 45)
        return region_names

    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    enabled_regions = get_enabled_aws_regions()
    print(f"\n💡 Ready-to-use list of regions: {enabled_regions}")

