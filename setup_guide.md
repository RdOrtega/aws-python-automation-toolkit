# ⚙️ Module 0: Setup & Authentication Guide

To run the scripts in this toolkit, you need to configure your local environment to communicate securely with your AWS account using Python and the **Boto3** SDK.

## 📋 Prerequisites
* Python 3.x installed on your machine.
* An active AWS Account.
* An IAM User with programmatic access (Access Key ID and Secret Access Key).

---

## 🛠️ Step 1: Install AWS CLI and Boto3

First, you need to install the AWS Command Line Interface (CLI) to manage your credentials securely, and Boto3, which is the AWS SDK for Python.

Open your terminal and run:

```bash
# Install AWS CLI (if not already installed)
# Download from: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

# Install Boto3 and python-dotenv
pip install boto3 python-dotenv
```

---

## 🔐 Step 2: Configure AWS Credentials

**Security Best Practice:** Never hardcode your Access Keys directly into your Python scripts. Instead, use the AWS CLI to store them securely on your local machine.

Run the following command in your terminal:

```bash
aws configure
```

The terminal will prompt you to enter your IAM user details. It should look like this:

```text
AWS Access Key ID [None]: YOUR_ACCESS_KEY_HERE
AWS Secret Access Key [None]: YOUR_SECRET_KEY_HERE
Default region name [None]: us-east-1  (Or your preferred region)
Default output format [None]: json
```

Boto3 will automatically search for these credentials in your system when you run any script.

---

## ✅ Step 3: Verify the Connection

To test if Python can successfully talk to your AWS account, create a temporary file named `test_connection.py` with this code and run it:

```python
import boto3

def test_aws_connection():
    try:
        # Connect to IAM service
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ Connection Successful!")
        print(f"👤 Connected as IAM User/Role ARN: {identity['Arn']}")
        print(f"🏢 AWS Account ID: {identity['Account']}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_aws_connection()
```

If it prints your Account ID, you are ready to start using the automation toolkit!
