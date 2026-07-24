# 🚀 Module 1: Amazon EC2 & Compute Automation

Welcome to the **EC2 & Compute Management** module. This directory contains production-ready Python scripts using **Boto3** (AWS SDK) designed to automate the complete lifecycle of virtual servers, firewall management, data retention, and cost-optimization strategies (FinOps).

---

## 📋 Module Overview & Scripts Summary

| Script | Core Function | Key AWS / Boto3 Features |
| :--- | :--- | :--- |
| **`01_create_ec2.py`** | Provisions a new EC2 instance | Uses waiters (`wait_until_running`) & Resource tags. |
| **`02_duplicate_ec2.py`** | Clones instances via AMI creation | Image generation with automated timestamps. |
| **`03_stop_ec2.py`** | Mass shutdowns based on Tags | FinOps cost-saving strategy using `filters`. |
| **`04_start_ec2.py`** | Mass boot-ups based on Tags | Schedule-driven instance startup automation. |
| **`05_terminate_ec2.py`** | Destroys instance permanently | Destruction verification via `wait_until_terminated`. |
| **`06_manage_security_groups.py`** | Configures cloud firewalls | Ingress rules authorization (SSH & HTTP ports). |
| **`07_ebs_snapshots.py`** | Automated backups & retention | Cross-timezone lifecycle cleanup & multi-tag filtering. |
| **`08_cleanup_resources.py`** | Sweeps orphaned AWS resources | Detects and releases unused EIPs & unattached EBS volumes. |

---

## 🛠️ Senior Architecture & Engineering Highlights

* **Idempotency & Resilience:** Scripts are designed with graceful error-handling (`ClientError`) to handle duplicate calls or missing resources cleanly without crashing pipeline executions.
* **AWS Lambda Ready (Hybrid Execution):** Key scripts (`07` & `08`) implement dual-entry logic using `lambda_handler` for Serverless cloud triggers (via EventBridge Cron) while maintaining local `__main__` execution support for local debugging.
* **FinOps-Driven Automation:** Includes automated resource sweepers (`08_cleanup_resources.py`) to eliminate silent, idle charges from detached EBS volumes and unallocated Elastic IPs.
* **Timezone Safety:** Backup retention calculations explicitly use `timezone.utc` to avoid offset mismatch issues between local system clocks and AWS servers.

---

## 💻 Prerequisites & Local Setup

Before executing any script in this module, ensure you have:

1. **Python 3.8+** installed.
2. **Boto3** library installed:
   ```bash
   pip install boto3
  ```
```bash
   aws configure
```





   
   
