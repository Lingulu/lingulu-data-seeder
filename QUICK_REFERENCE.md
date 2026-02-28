# Quick Reference - Lingulu Data Seeder

Quick reference for commonly used commands.

## 🚀 Initial Setup (One Time Only)

### 1. Clone & Setup Environment
```bash
cd c:\Users\mario\Code\Projects\Lingulu\lingulu-data-seeder
python -m venv env
.\env\Scripts\Activate.ps1          # Windows PowerShell
# or
.\env\Scripts\activate.bat          # Windows CMD
# or
source env/bin/activate              # Linux/Mac

pip install -r requirements.txt
```

### 2. Setup Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env with your preferred editor
notepad .env                         # Windows
nano .env                            # Linux/Mac
```

### 3. Setup AWS CLI (Optional)
```bash
aws configure
# Enter: Access Key, Secret Key, Region, Format
```

## 📡 SSH Tunnel Commands

### Setup SSH Tunnel (3 Options)

**Option 1: PowerShell Script (Recommended for Windows)**
```powershell
# Edit configuration in setup-ssh-tunnel.ps1 first
.\setup-ssh-tunnel.ps1
```

**Option 2: Batch Script (Windows alternative)**
```cmd
# Edit configuration in setup-ssh-tunnel.bat first
setup-ssh-tunnel.bat
```

**Option 3: Bash Script (Linux/Mac)**
```bash
# Edit configuration in setup-ssh-tunnel.sh first
chmod +x setup-ssh-tunnel.sh
./setup-ssh-tunnel.sh
```

**Option 4: Manual SSH Command**
```bash
# Windows
ssh -i "C:\Users\mario\.ssh\your-key.pem" -L 5432:your-rds-endpoint.region.rds.amazonaws.com:5432 ec2-user@your-ec2-ip -N

# Linux/Mac
ssh -i ~/.ssh/your-key.pem -L 5432:your-rds-endpoint.region.rds.amazonaws.com:5432 ec2-user@your-ec2-ip -N
```

### Stop SSH Tunnel
```
Press Ctrl+C in the terminal running the tunnel
```

## 🧪 Testing Commands

### Test SSH Connection to EC2
```bash
ssh -i "C:\Users\mario\.ssh\your-key.pem" ec2-user@your-ec2-ip
# If successful, exit with: exit
```

### Test Database Connection from EC2
```bash
# From within EC2 (after SSH login)
psql -h your-rds-endpoint.region.rds.amazonaws.com -U your_db_user -d your_db_name
# Exit with: \q
```

### Test Database Connection from Local (via SSH Tunnel)
```bash
# Make sure SSH tunnel is already running
python test-connection.py
```

### Test S3 Access
```bash
# List S3 buckets
aws s3 ls

# List contents of specific bucket
aws s3 ls s3://lingulu-course

# Test upload file
echo "test" > test.txt
aws s3 cp test.txt s3://lingulu-course/test.txt
aws s3 rm s3://lingulu-course/test.txt
rm test.txt
```

## 🌱 Seeder Commands

### Run Seeder
```bash
# Make sure SSH tunnel is active and test-connection.py succeeded
python main.py
```

### Check Database After Seeding
```bash
# Via psql (if installed)
psql -h localhost -p 5432 -U your_db_user -d your_db_name

# Query examples:
SELECT count(*) FROM courses;
SELECT count(*) FROM lessons;
SELECT count(*) FROM materi;
SELECT count(*) FROM quiz;
```

## 🔧 Troubleshooting Commands

### Check if Port is in Use (Windows)
```powershell
# Check port 5432
netstat -ano | findstr :5432
```

### Check if Port is in Use (Linux/Mac)
```bash
# Check port 5432
lsof -i :5432
# or
netstat -an | grep 5432
```

### Kill Process on Port (Windows)
```powershell
# Get PID from netstat output, then:
taskkill /PID <PID> /F
```

### Kill Process on Port (Linux/Mac)
```bash
# Get PID from lsof output, then:
kill -9 <PID>
```

### Check EC2 Instance Status
```bash
# Via AWS CLI
aws ec2 describe-instances --instance-ids i-xxxxxxxxxxxxxxxxx --query 'Reservations[0].Instances[0].State.Name'
```

### Check RDS Instance Status
```bash
# Via AWS CLI
aws rds describe-db-instances --db-instance-identifier your-db-identifier --query 'DBInstances[0].DBInstanceStatus'
```

### Verify AWS Credentials
```bash
# Check current AWS identity
aws sts get-caller-identity

# Test S3 permissions
aws s3 ls s3://lingulu-course
```

### Check Python Environment
```bash
# Check Python version
python --version

# Check if venv is activated (should show env path)
which python       # Linux/Mac
where python       # Windows

# List installed packages
pip list

# Verify specific package
pip show psycopg2
pip show boto3
```

## 📦 Package Management

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt    # Update requirements.txt
```

### Reinstall All Dependencies
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 🗂️ File Operations

### Check File Structure
```bash
# Windows
tree /F MATERI

# Linux/Mac
tree MATERI
# or
find MATERI -type f
```

### Count Files in Directory
```bash
# Windows PowerShell
(Get-ChildItem -Path MATERI -Recurse -File).Count

# Linux/Mac
find MATERI -type f | wc -l
```

## 🔐 Security & Credentials

### Set PEM Key Permissions (Linux/Mac)
```bash
chmod 400 ~/.ssh/your-key.pem
```

### Rotate AWS Credentials
```bash
# Update .env file with new credentials
# Test credentials
aws s3 ls

# Reconfigure AWS CLI
aws configure
```

## 📊 Monitoring

### Monitor S3 Upload Progress (during seeding)
```bash
# In another terminal
watch -n 2 'aws s3 ls s3://lingulu-course --recursive | wc -l'
```

### Monitor Database Size
```sql
-- Connect to database first
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 🆘 Emergency Commands

### Rollback Database (if needed)
```sql
-- Truncate all tables (WARNING: DELETES ALL DATA!)
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
```

### Stop All SSH Connections
```bash
# Windows
taskkill /IM ssh.exe /F

# Linux/Mac
pkill ssh
```

### Clear S3 Bucket (WARNING: DELETES ALL FILES!)
```bash
# Remove all objects from bucket
aws s3 rm s3://lingulu-course --recursive

# Verify deletion
aws s3 ls s3://lingulu-course
```

## 🔄 Daily Workflow

### Recommended Workflow
```bash
# 1. Activate virtual environment
.\env\Scripts\Activate.ps1          # Windows
source env/bin/activate              # Linux/Mac

# 2. Start SSH tunnel (terminal 1)
.\setup-ssh-tunnel.ps1              # Windows
./setup-ssh-tunnel.sh               # Linux/Mac

# 3. Test connection (terminal 2)
python test-connection.py

# 4. If test passed, run seeder
python main.py

# 5. After done, stop SSH tunnel (terminal 1)
# Press Ctrl+C
```

## 📝 Useful SQL Queries

### Get Table Row Counts
```sql
SELECT 
    schemaname,
    tablename,
    n_tup_ins AS "inserts",
    n_tup_upd AS "updates",
    n_tup_del AS "deletes",
    n_live_tup AS "live_rows"
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

### Check Last Seeded Data
```sql
-- Assuming you have created_at timestamp columns
SELECT tablename, MAX(created_at) as last_insert
FROM (
    SELECT 'courses' as tablename, MAX(created_at) as created_at FROM courses
    UNION ALL
    SELECT 'lessons', MAX(created_at) FROM lessons
    UNION ALL
    SELECT 'materi', MAX(created_at) FROM materi
    UNION ALL
    SELECT 'quiz', MAX(created_at) FROM quiz
) t
GROUP BY tablename;
```

## 🔗 Useful Links

- AWS Console: https://console.aws.amazon.com
- AWS RDS: https://console.aws.amazon.com/rds
- AWS EC2: https://console.aws.amazon.com/ec2
- AWS S3: https://console.aws.amazon.com/s3
- AWS IAM: https://console.aws.amazon.com/iam

---

**Created:** February 28, 2026  
**Project:** Lingulu Data Seeder  
**Purpose:** Quick reference for common commands
