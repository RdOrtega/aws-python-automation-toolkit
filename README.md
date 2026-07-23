# AWS EC2 Lifecycle Manager with Python ☁️🐍

This project demonstrates my ability to manage AWS infrastructure programmatically using Python and the **Boto3** SDK. As an IT Support & Cloud Operations professional, I built this script to automate the full lifecycle of EC2 instances (creation, monitoring, state management), which is crucial for cost optimization and operational efficiency.

## 🚀 Features

- **Provisioning:** Creates new EC2 instances with specific `Tags` automatically applied.
- **Auditing:** Lists all EC2 instances in the region along with their current states (Running, Stopped, Terminated).
- **State Management:** Quickly `Start`, `Stop`, or `Terminate` instances by ID to prevent idle resources from generating costs.
- **Error Handling:** Implements `botocore.exceptions` for clean error reporting.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **AWS SDK:** Boto3
* **Concepts:** Infrastructure as Code (IaC) principles, AWS Well-Architected Framework (Cost Optimization), Object-Oriented Programming (OOP).

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
4. Run the script:
   ```bash
   python manage_ec2.py
   ```

## 📸 Proof of Concept

*(Nota: Aquí subiremos las capturas de pantalla de la terminal y AWS más adelante)*

---
*Created by Rubén Darío Ortega - L2 IT Support Specialist & Cloud Operations.*
