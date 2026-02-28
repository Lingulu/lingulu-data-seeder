# Lingulu Data Seeder

Script for seeding data to PostgreSQL database (AWS RDS) and uploading files to S3.

## 📚 Documentation

- **[README.md](README.md)** - Main guide (this file)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Connection architecture diagram and explanation
- **[CHECKLIST.md](CHECKLIST.md)** - Complete checklist before running seeder
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference for common commands

## Prerequisites

- Python 3.x
- Virtual environment (venv)
- AWS CLI configured with valid credentials
- Access to EC2 instance connected to RDS network
- PEM private key for SSH to EC2
- Security groups configured correctly

## Quick Start

### Available Helper Scripts

1. **`setup-ssh-tunnel.ps1`** (Windows PowerShell) / **`setup-ssh-tunnel.bat`** (Windows Batch) / **`setup-ssh-tunnel.sh`** (Linux/Mac)
   - Automated script to create SSH tunnel
   - Edit configuration at the top of the file before using

2. **`test-connection.py`**
   - Script to test database connection
   - Run before running seeder to ensure connection is successful

3. **`.env.example`**
   - Template for `.env` file
   - Copy and rename to `.env`, then fill with correct credentials

### Quick Workflow

1. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with correct credentials
   ```

2. **Edit and run SSH tunnel:**
   
   **Windows (PowerShell):**
   ```powershell
   # Edit setup-ssh-tunnel.ps1 with your AWS configuration
   .\setup-ssh-tunnel.ps1
   ```
   
   **Windows (Batch - if PowerShell has issues):**
   ```cmd
   # Edit setup-ssh-tunnel.bat with your AWS configuration
   setup-ssh-tunnel.bat
   # Or double-click setup-ssh-tunnel.bat file
   ```
   
   **Linux/Mac:**
   ```bash
   # Edit setup-ssh-tunnel.sh with your AWS configuration
   chmod +x setup-ssh-tunnel.sh
   ./setup-ssh-tunnel.sh
   ```

3. **Test connection (in new terminal):**
   ```bash
   # Activate virtual environment first
   python test-connection.py
   ```

4. **Run seeder (if test passed):**
   ```bash
   python main.py
   ```

---

**💡 Tips:** For more detailed and systematic guide, see [CHECKLIST.md](CHECKLIST.md) which provides a complete step-by-step checklist.

## Installing Dependencies

1. **Clone repository and navigate to project directory:**
   ```bash
   cd c:\Users\mario\Code\Projects\Lingulu\lingulu-data-seeder
   ```

2. **Activate virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   .\env\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   .\env\Scripts\activate.bat
   ```
   
   **Linux/Mac:**
   ```bash
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables Configuration

### 1. Setup `.env` File

Create a `.env` file in the project root directory with the following content:

```env
# PostgreSQL Configuration (AWS RDS)
LINGULU_DB_HOST=localhost
LINGULU_DB_PORT=5432
LINGULU_DB_USER=your_db_username
LINGULU_DB_PASSWORD=your_db_password
LINGULU_DB_NAME=your_db_name

# AWS S3 Configuration
LINGULU_S3_BUCKET_NAME=lingulu-course
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=ap-southeast-1
```

**Note:**
- `LINGULU_DB_HOST` is set to `localhost` because we will use SSH tunneling
- `LINGULU_DB_PORT` is the local port that will be forwarded (default: 5432)

### 2. Setup AWS Credentials

Ensure AWS credentials are configured for S3 access:

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (example: ap-southeast-1)
- Default output format (example: json)

## AWS RDS Private Access Configuration

> 📖 **Reference:** For visual diagram and detailed architecture explanation, see [ARCHITECTURE.md](ARCHITECTURE.md)

### Connection Architecture

```
[Local Machine] --SSH--> [EC2 Instance] --Private Network--> [RDS PostgreSQL]
                 (PEM Key)              (Security Group)
```

### 1. Setup Security Groups

#### EC2 Security Group:
- **Inbound Rules:**
  - SSH (Port 22) from your public IP
  - PostgreSQL (Port 5432) from local IP for testing (optional)
  
- **Outbound Rules:**
  - All traffic (or minimum access to RDS security group)

#### RDS Security Group:
- **Inbound Rules:**
  - PostgreSQL (Port 5432) from EC2 Security Group
  
- **Outbound Rules:**
  - All traffic (default)

### 2. Setup SSH Tunneling to EC2

#### a. Save PEM Private Key

1. Download PEM key from AWS Console (when creating EC2 key pair)
2. Save in a secure location, for example: `C:\Users\mario\.ssh\lingulu-ec2-key.pem`
3. Set permissions (Linux/Mac):
   ```bash
   chmod 400 ~/.ssh/lingulu-ec2-key.pem
   ```

#### b. Required Information

- **EC2 Public IP/DNS:** Check in AWS Console > EC2 > Instances
- **EC2 Username:** Usually `ec2-user` (Amazon Linux), `ubuntu` (Ubuntu), or `admin` (Debian)
- **RDS Endpoint:** Check in AWS Console > RDS > Databases > Connectivity & security
- **RDS Port:** Default 5432 for PostgreSQL

### 3. Creating SSH Tunnel

#### Windows (PowerShell/Command Prompt):
```bash
ssh -i "C:\Users\mario\.ssh\lingulu-ec2-key.pem" -L 5432:your-rds-endpoint.region.rds.amazonaws.com:5432 ec2-user@your-ec2-public-ip -N
```

#### Linux/Mac:
```bash
ssh -i ~/.ssh/lingulu-ec2-key.pem -L 5432:your-rds-endpoint.region.rds.amazonaws.com:5432 ec2-user@your-ec2-public-ip -N
```

**Parameter Explanation:**
- `-i`: Path to PEM private key
- `-L`: Local port forwarding (format: `local_port:rds_endpoint:rds_port`)
- `ec2-user@your-ec2-public-ip`: SSH connection to EC2
- `-N`: Don't execute command, only forwarding

**Concrete Example:**
```bash
ssh -i "C:\Users\mario\.ssh\lingulu-ec2-key.pem" -L 5432:lingulu-db.ch1234567890.ap-southeast-1.rds.amazonaws.com:5432 ec2-user@13.123.45.67 -N
```

**Tips:**
- Run this command in a separate terminal and keep it running
- If port 5432 is already in use, use another port (e.g., 5433) and adjust in `.env`

### 4. Verify Connection

#### a. Test SSH to EC2

```bash
ssh -i "C:\Users\mario\.ssh\lingulu-ec2-key.pem" ec2-user@your-ec2-public-ip
```

If successful, you will be logged into the EC2 instance. Exit with `exit`.

#### b. Test Database Connection from EC2

From within the EC2 instance:
```bash
psql -h your-rds-endpoint.region.rds.amazonaws.com -U your_db_user -d your_db_name
```

Enter password if prompted.

#### c. Test SSH Tunnel

After SSH tunnel is running, test from local machine:

**Using psql:**
```bash
psql -h localhost -p 5432 -U your_db_user -d your_db_name
```

**Using Python:**
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="your_db_user",
    password="your_db_password",
    dbname="your_db_name"
)
print("Connection successful!")
conn.close()
```

## Running the Seeder Script

### 1. Ensure SSH Tunnel is Active

Open a new terminal and run the SSH tunnel using the helper script or manually (see previous section).

### 2. Test Database Connection

Before running the seeder, test the connection first:

```bash
python test-connection.py
```

Ensure the output shows "✓ KONEKSI BERHASIL!" before continuing.

### 3. Run Seeder Script

In a separate terminal with virtual environment active:

```bash
python main.py
```

### 4. Process Flow

The script will:
1. **Truncate all tables** in the database (CASCADE)
2. **Seed courses data** to database
3. **Upload audio files** from `MATERI/audio-materi/` to S3
4. **Seed lessons data** to database
5. **Upload markdown files** from `MATERI/file-markdown-materi/` to S3
6. **Seed materi data** to database
7. **Upload quiz data** from `MATERI/pilihan-ganda/` to S3
8. **Seed quiz data** to database

**⚠️ WARNING:** This script will **delete all data** in the database before seeding. Make sure you run it in the correct environment!

## Troubleshooting

### Error: "Connection refused"
- Ensure SSH tunnel is still running
- Check if the port being used is correct
- Verify RDS endpoint and port

### Error: "Permission denied (publickey)"
- Check PEM key path is correct
- Ensure PEM key permissions are correct (400)
- Verify EC2 username (ec2-user, ubuntu, admin, etc.)

### Error: "Connection timeout"
- Check EC2 Security Group allows SSH from your IP
- Verify EC2 instance is running
- Check if EC2 has a public IP

### Error: "Could not connect to server"
- Verify RDS Security Group allows access from EC2
- Check if RDS endpoint is correct
- Ensure EC2 and RDS are in the same VPC/subnet or connected

### Error S3 Upload Failed
- Check AWS credentials are configured
- Verify IAM user has S3 permissions
- Ensure bucket name is correct

## MATERI Directory Structure

```
MATERI/
├── audio-materi/
│   └── courses/
│       ├── course-1/
│       ├── course-2/
│       └── course-3/
├── file-markdown-materi/
│   ├── course-1/
│   │   ├── lesson1-1/
│   │   ├── lesson1-2/
│   │   ├── lesson1-3/
│   │   └── lesson1-4/
│   ├── course-2/
│   └── course-3/
└── pilihan-ganda/
    ├── course-1/
    ├── course-2/
    └── course-3/
```

Ensure all files are available in the appropriate directories before running the script.

## Security Notes

1. **Don't commit `.env` file** to repository (already in `.gitignore`)
2. **Store PEM key in a secure location** and don't share
3. **Use IAM user with least privilege** for AWS
4. **Rotate credentials regularly**
5. **Use different environments** for development and production

## Recommended Workflow

1. **Development:** Use local PostgreSQL or RDS development
2. **Staging:** Use RDS staging with SSH tunnel
3. **Production:** Use automation/CI-CD, not manual seeding

---

**Created for:** Lingulu Project  
**Last updated:** February 28, 2026
