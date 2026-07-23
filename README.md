# AWS Cloud Automation Toolkit (Python + Boto3) ☁️🐍

This repository is a comprehensive collection of Python scripts designed to automate and manage core AWS services. As an IT Support & Cloud Operations professional, I built this toolkit to demonstrate Infrastructure as Code (IaC) principles, operational efficiency, and programmatic cloud management.

## 🗂️ Project Structure

This project is divided into modular sections based on AWS services. 

### ⚙️ Module 0: Setup & Authentication
Before running any script, you need to connect Python to your AWS environment.
* **Guide:** [How to install Boto3 and configure AWS CLI credentials.](setup_guide.md)

### 🖥️ Module 1: EC2 (Compute) & Cost Optimization
Scripts to manage virtual servers and prevent unnecessary cloud spending.
* `01_create_ec2.py`: Provision and configure a new EC2 instance.
* `02_duplicate_ec2.py`: Create an AMI (Image) from an existing instance and launch a clone.
* `03_stop_ec2.py`: Pause/Stop an instance to save costs.
* `04_start_ec2.py`: Activate/Start a stopped instance.
* `05_terminate_ec2.py`: Permanently delete an instance.
* `06_manage_security_groups.py`: Create firewalls and open ports (e.g., SSH, HTTP).
* `07_ebs_snapshots.py`: Automate backups by creating snapshots of EC2 volumes.
* `08_cleanup_resources.py`: **[Cost Saving]** Find and delete unattached EBS volumes and unused Elastic IPs.

### 🪣 Module 2: S3 (Storage) Operations
Scripts to handle scalable cloud storage, granular security, and backups.
* `01_create_bucket.py`: Provision a new S3 bucket with secure policies.
* `02_upload_files.py`: Automate file/backup uploads to S3.
* `03_manage_objects.py`: List, download, or delete objects within a bucket.
* `04_presigned_urls.py`: Generate temporary, secure download links for private files.
* `05_folder_permissions.py`: Configure Bucket Policies for View-Only access to specific prefixes (folders).
* `06_lifecycle_rules.py`: Automate archiving of old files to S3 Glacier to reduce costs.

### 🔐 Module 3: IAM (Identity & Access Management)
Scripts to manage user lifecycles and enforce Zero Trust security.
* `01_create_user.py`: Programmatically create a new IAM user and attach policies.
* `02_audit_keys.py`: **[Security]** Find users with Access Keys older than 90 days.
* `03_offboard_user.py`: Safely delete a user, detach policies, and remove access keys.

### 📊 Module 4: CloudWatch (Monitoring & Alerts)
Scripts to monitor infrastructure health and react to events.
* `01_create_cpu_alarm.py`: Create an alarm that triggers when EC2 CPU exceeds 80%.
* `02_billing_alarm.py`: Set up alerts when estimated AWS charges exceed a specific threshold.

### ⚡ Module 5: Lambda (Serverless Computing)
Scripts to deploy and trigger serverless functions.
* `01_deploy_lambda.py`: Zip a local Python script and deploy it to AWS Lambda.
* `02_invoke_lambda.py`: Trigger a Lambda function programmatically.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **AWS SDK:** Boto3
* **Concepts:** Cloud Provisioning, Cost Optimization, Security & Identity (Zero Trust), Serverless, Monitoring.

## ⚙️ How to Use

1. Clone the repository.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your AWS credentials are set up in your terminal:
   ```bash
   aws configure
   ```
4. Run any script from its respective module folder:
   ```bash
   python Module_1_EC2/01_create_ec2.py
   ```

## 📸 Proof of Concept

*(Nota: Aquí subiremos las capturas de pantalla de la terminal y AWS más adelante)*

---
*Created by Rubén Darío Ortega - L2 IT Support Specialist & Cloud Operations.*
