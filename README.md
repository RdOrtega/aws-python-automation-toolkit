
# ☁️🐍 AWS Cloud Automation Toolkit (Python + Boto3)

Welcome to the **AWS Cloud Automation Toolkit**, an enterprise-ready repository designed to automate cloud infrastructure operations, enforce Zero Trust security, optimize monthly AWS billing (FinOps), and maintain operational compliance using **Python** and **Boto3**.

This toolkit reflects real-world Cloud Operations and System Administration scenarios, focusing on resilience, security auditing, automated cost savings, and serverless orchestration.

---

## 🗂️ Project Structure & Capabilities

### 🖥️ Module 1: EC2 (Compute) & Auto Scaling

Scripts to manage virtual server lifecycles, scaling strategies, and FinOps cost sweeping.

- 01_create_ec2.py: Provision and tag new EC2 instances.
- 02_duplicate_ec2.py: Clone instances via automated AMI generation.
- 03_stop_ec2.py: Mass shutdown based on resource tags for cost savings.
- 04_start_ec2.py: Schedule-driven instance startup automation.
- 05_terminate_ec2.py: Controlled resource destruction with wait verification.
- 06_manage_security_groups.py: Configure cloud firewalls and ingress rules.
- 07_ebs_snapshots.py: Automated volume backups and retention lifecycle.
- 08_cleanup_resources.py: [FinOps] Detect and purge unattached EBS volumes and unused Elastic IPs.
- 09_auto_scaling_management.py: Dynamically adjust Auto Scaling Group (ASG) capacity limits.
- 10_list_enabled_regions.py: Query AWS global endpoints for active regions in your account.
- 11_ec2_health_check_report.py: Audit system status checks and export multi-region instance health reports.
- 12_change_instance_type.py: Automate vertical scaling (resize instance types safely).
