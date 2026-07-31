
import boto3
import time
from botocore.exceptions import ClientError

def get_instance_id_by_name(ec2_client, server_name):
    """
    Helper function: Searches AWS for an active instance matching the given Name tag.
    """
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [server_name]},
                {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
            ]
        )
        
        # Extraemos las instancias encontradas
        instances = [
            instance['InstanceId']
            for reservation in response['Reservations']
            for instance in reservation['Instances']
        ]

        if not instances:
            print(f"❌ Error: No se encontró ninguna instancia con el nombre '{server_name}'.")
            return None

        # Tomamos la primera coincidencia
        found_id = instances[0]
        print(f"🎯 Encontrado! El servidor '{server_name}' tiene el ID: {found_id}")
        return found_id

    except ClientError as e:
        print(f"❌ Error buscando la instancia: {e}")
        return None


def duplicate_instance(source_server_name, clone_name, assigned_to, iam_profile_name):
    """
    Finds a source server by Name tag, creates an AMI, 
    and launches a new cloned instance with SSM profile and tags.
    """
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')

    try:
        # Step 0: Resolviendo el ID a partir del Nombre
        print(f"🔍 Buscando el servidor modelo '{source_server_name}'...")
        source_instance_id = get_instance_id_by_name(ec2_client, source_server_name)
        
        if not source_instance_id:
            print("🛑 Proceso abortado: No se pudo identificar el servidor origen.")
            return None

        # Step 1: Create the Image (AMI) from the source instance ID
        print(f"📸 Step 1: Creating AMI from source instance {source_instance_id}...")
        image_response = ec2_client.create_image(
            InstanceId=source_instance_id,
            Name=f"Clone-AMI-{source_server_name}-{int(time.time())}",
            Description="Automated clone image created via Python",
            NoReboot=True  # Prevents source server downtime
        )
        
        image_id = image_response['ImageId']
        print(f"⏳ Waiting for AMI {image_id} to be available...")
        
        # Wait until AMI processing finishes
        waiter = ec2_client.get_waiter('image_available')
        waiter.wait(ImageIds=[image_id])
        print("✅ AMI is ready!")

        # Step 2: Launch the Clone with IAM Profile and Tags
        print("🚀 Step 2: Launching clone instance...")
        instances = ec2_resource.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            IamInstanceProfile={
                'Name': iam_profile_name
            },
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': clone_name},
                        {'Key': 'AssignedTo', 'Value': assigned_to},
                        {'Key': 'ClonedFrom', 'Value': source_server_name}  # Trazabilidad por nombre
                    ]
                }
            ]
        )
        
        clone = instances[0]
        print(f"⏳ Waiting for clone instance {clone.id} to be running...")
        clone.wait_until_running()
        clone.reload()
        
        print(f"✅ Success! Clone {clone.id} is RUNNING.")
        if clone.public_ip_address:
            print(f"🌐 Clone Public IP: {clone.public_ip_address}")
            
        return clone.id

    except ClientError as e:
        print(f"❌ AWS API Error: {e}")
        return None


if __name__ == "__main__":
    # 📌 NOMBRE del servidor modelo en AWS que quieres copiar (tal como aparece en la columna Name)
    SOURCE_SERVER_NAME = 'Dev-Tech-AppServer-01' 
    
    # 👤 Datos para la nueva máquina que le vas a entregar al usuario
    CLONE_SERVER_NAME = 'Slalom-Workstation-Carlos'
    ASSIGNED_TO = 'Carlos_Luis'
    IAM_PROFILE = 'SSM-EC2-Role'
    
    print("🔄 Starting EC2 Duplication Script...")
    duplicate_instance(
        source_server_name=SOURCE_SERVER_NAME, 
        clone_name=CLONE_SERVER_NAME, 
        assigned_to=ASSIGNED_TO, 
        iam_profile_name=IAM_PROFILE
    )
