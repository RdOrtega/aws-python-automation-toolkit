
# Reusamos la función del script 01
from 01_create_base_ec2 import create_ec2_instance

if __name__ == "__main__":
    # 📌 Pegas aquí el ID que te imprimió en pantalla el script 02
    CUSTOM_AMI_ID = 'ami-0a1b2c3d4e5f67890' 
    
    print("🚀 Deploying workstations from Golden AMI...")
    
    # Usuario 1: Carlos
    create_ec2_instance(
        image_id=CUSTOM_AMI_ID,
        instance_type='t2.micro',
        tag_name='Slalom-Workstation-Carlos',
        assigned_to='Carlos_Luis',
        iam_profile_name='SSM-EC2-Role'
    )

    # Usuario 2: Laura
    create_ec2_instance(
        image_id=CUSTOM_AMI_ID,
        instance_type='t2.micro',
        tag_name='Slalom-Workstation-Laura',
        assigned_to='Laura_Gomez',
        iam_profile_name='SSM-EC2-Role'
    )
