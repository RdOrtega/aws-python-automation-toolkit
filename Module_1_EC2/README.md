# 🚀 Module 1: Amazon EC2 & Compute Automation

Welcome to the **EC2 & Compute Management** module. This directory contains Python scripts using **Boto3** (AWS SDK) designed to automate the complete lifecycle of virtual servers — provisioning, imaging, firewall management, backup retention, cost-optimization (FinOps), and safe decommissioning.

---

## 📋 Module Overview & Scripts Summary

| Script | Core Function | Key AWS / Boto3 Features |
|---|---|---|
| `00_list_enabled_regions.py` | Queries active AWS regions | Account-level endpoint discovery via `describe_regions`. |
| `01_create_ec2.py` | Provisions a new EC2 instance | Uses waiters (`wait_until_running`) & resource tags. |
| `02_create_ami.py` | Creates a reusable AMI from an existing instance | Image generation with automated timestamps. |
| `03_deploy_from_ami.py` | Launches new instances from a custom AMI | Template-based provisioning for repeatable deployments. |
| `04_start_ec2.py` | Mass boot-ups based on tags | Schedule-driven instance startup automation. |
| `05_stop_ec2.py` | Mass shutdowns based on tags | FinOps cost-saving strategy using `filters`. |
| `06_manage_security_groups.py` | Configures cloud firewalls | Ingress rules authorization (SSH & HTTP ports). |
| `07_ebs_snapshots.py` | Automated backups & retention | Cross-timezone lifecycle cleanup & multi-tag filtering. |
| `08_cleanup_resources.py` | Sweeps orphaned AWS resources | Detects and releases unused EIPs & unattached EBS volumes. |
| `09_auto_scaling_management.py` | Adjusts Auto Scaling limits | Modifies ASG capacity parameters (`DesiredCapacity`, `MinSize`, `MaxSize`). |
| `10_ec2_health_check_report.py` | Multi-region health audit | Evaluates system & instance checks using `describe_instance_status`. |
| `11_change_instance_type.py` | Resizes instances safely | Vertical scaling automation using state waiters and `modify_instance_attribute`. |
| `12_terminate_ec2.py` | Destroys instance permanently | Destruction verification via `wait_until_terminated`. |

---

## 🛠️ Engineering Highlights

- **Error Handling:** Scripts catch `ClientError` explicitly, printing clean, human-readable failure messages instead of raw tracebacks — useful for automation pipelines where a crash shouldn't halt an entire workflow.
- **Tag-Driven Resource Management:** Instances are provisioned and filtered using custom tags (e.g. `Area`, `AssignedTo`), enabling per-user or per-department tracking and lifecycle control (start/stop/terminate by owner).
- **FinOps-Oriented Automation:** `08_cleanup_resources.py` targets idle, unbilled-but-costly resources — detached EBS volumes and unallocated Elastic IPs — that commonly go unnoticed in manual AWS management.
- **State-Aware Operations:** Scripts that modify running infrastructure (`07`, `11`, `12`) rely on **waiters** to confirm state transitions before proceeding, avoiding race conditions common in async cloud operations.

> 💡 *Note: if any script here also supports a `lambda_handler` for serverless/EventBridge triggers, or explicit `timezone.utc` handling in `07_ebs_snapshots.py`, add a bullet for it — but only once it's actually implemented in the code, since these are the kinds of claims interviewers tend to ask you to walk through live.*

---

## 💻 Prerequisites & Local Setup

Before executing any script in this module, ensure you have:

**1. Boto3 library installed:**
```bash
pip install boto3
```

**2. AWS CLI credentials configured:**
```bash
aws configure
```

**3. IAM permissions** scoped to EC2 (and related services — Auto Scaling, EBS, VPC) for the credentials/role you're using to run these scripts.

---

## 📁 Usage

Each script can be run independently:

```bash
python 01_create_ec2.py
```

Scripts that operate on existing resources (e.g. `04`–`09`, `11`, `12`) typically filter by tags — review the script's configuration section before running against production resources.
