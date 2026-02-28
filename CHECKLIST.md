# Complete Checklist Before Running Seeder

Use this checklist to ensure all configurations are correct before running the seeder script.

## ☑️ Pre-Setup Checklist

### 1. AWS Account & Resources
- [ ] Have access to AWS Console
- [ ] RDS PostgreSQL instance already created
- [ ] EC2 instance already created and running
- [ ] S3 bucket already created (name: `lingulu-course` or as needed)
- [ ] IAM user with permissions:
  - [ ] S3 full access (or minimum s3:PutObject)
  - [ ] Access key & secret key already created

### 2. Security Groups
- [ ] **EC2 Security Group:**
  - [ ] Inbound: SSH (port 22) from your public IP
  - [ ] Outbound: All traffic or minimum PostgreSQL (5432) to RDS
  
- [ ] **RDS Security Group:**
  - [ ] Inbound: PostgreSQL (port 5432) from EC2 security group
  - [ ] Outbound: Default (all traffic)

### 3. Network Configuration
- [ ] EC2 and RDS are in the same VPC or connected
- [ ] EC2 has public IP (for SSH from local)
- [ ] RDS in private subnet (no public IP needed)

### 4. SSH Access
- [ ] PEM private key already downloaded from AWS
- [ ] PEM key stored in secure location (example: `~/.ssh/`)
- [ ] (Linux/Mac) PEM key permissions already set to 400: `chmod 400 key.pem`

## ☑️ Local Setup Checklist

### 1. Python Environment
- [ ] Python 3.x installed
- [ ] Virtual environment already created: `python -m venv env`
- [ ] Virtual environment already activated:
  - [ ] Windows: `.\env\Scripts\Activate.ps1` or `.\env\Scripts\activate.bat`
  - [ ] Linux/Mac: `source env/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`

### 2. Environment Variables (.env)
- [ ] File `.env` already created (copy from `.env.example`)
- [ ] Database (DB) configuration:
  - [ ] `LINGULU_DB_HOST=localhost` ✓
  - [ ] `LINGULU_DB_PORT=5432` (or other port chosen)
  - [ ] `LINGULU_DB_USER=<your_rds_username>`
  - [ ] `LINGULU_DB_PASSWORD=<your_rds_password>`
  - [ ] `LINGULU_DB_NAME=<database_name>`
  
- [ ] AWS S3 configuration:
  - [ ] `LINGULU_S3_BUCKET_NAME=lingulu-course` (or your bucket name)
  - [ ] `AWS_ACCESS_KEY_ID=<your_access_key>`
  - [ ] `AWS_SECRET_ACCESS_KEY=<your_secret_key>`
  - [ ] `AWS_DEFAULT_REGION=ap-southeast-1` (or your region)

### 3. AWS CLI (Optional but Recommended)
- [ ] AWS CLI installed
- [ ] AWS CLI configured: `aws configure`
- [ ] Test S3 access: `aws s3 ls s3://lingulu-course`

### 4. Data Files
- [ ] Folder `MATERI/` complete with structure:
  - [ ] `MATERI/audio-materi/courses/course-1/`
  - [ ] `MATERI/audio-materi/courses/course-2/`
  - [ ] `MATERI/audio-materi/courses/course-3/`
  - [ ] `MATERI/file-markdown-materi/course-1/lesson1-1/`
  - [ ] `MATERI/file-markdown-materi/course-2/lesson2-1/`
  - [ ] `MATERI/file-markdown-materi/course-3/lesson3-1/`
  - [ ] `MATERI/pilihan-ganda/course-1/lesson1-1/`
  - [ ] `MATERI/pilihan-ganda/course-2/lesson2-1/`
  - [ ] `MATERI/pilihan-ganda/course-3/lesson3-1/`

## ☑️ Connection Checklist

### 1. Test SSH Connection to EC2
```bash
ssh -i path/to/your-key.pem ec2-user@<EC2_PUBLIC_IP>
```
- [ ] Successfully logged into EC2
- [ ] No "Permission denied" or "Connection refused" errors
- [ ] Can exit with `exit`

**Troubleshooting if failed:**
- Check EC2 IP is correct
- Check username matches (ec2-user, ubuntu, admin, etc.)
- Check PEM key path is correct
- Check EC2 Security Group allows SSH from your IP

### 2. Test Connection from EC2 to RDS
Login to EC2, then test:
```bash
# Install psql if not available
sudo yum install postgresql -y  # Amazon Linux
# or
sudo apt-get install postgresql-client -y  # Ubuntu

# Test connection
psql -h <RDS_ENDPOINT> -U <DB_USER> -d <DB_NAME>
```
- [ ] Successfully connected to database from within EC2
- [ ] Can execute test query: `SELECT version();`

**Troubleshooting if failed:**
- Check RDS endpoint is correct
- Check RDS security group allows from EC2
- Check database username and password

### 3. Setup SSH Tunnel
Edit configuration in `setup-ssh-tunnel.ps1` / `setup-ssh-tunnel.bat` / `setup-ssh-tunnel.sh`:
- [ ] `PEM_KEY_PATH` is correct
- [ ] `EC2_USER` matches
- [ ] `EC2_PUBLIC_IP` is correct
- [ ] `RDS_ENDPOINT` is correct
- [ ] `RDS_PORT` is correct (default: 5432)
- [ ] `LOCAL_PORT` matches `LINGULU_DB_PORT` in `.env`

Run SSH tunnel:
- [ ] Windows: `.\setup-ssh-tunnel.ps1` or `setup-ssh-tunnel.bat`
- [ ] Linux/Mac: `./setup-ssh-tunnel.sh`
- [ ] Terminal stays open (don't close it)
- [ ] No errors

### 4. Test Database Connection from Local
In a new terminal (keep SSH tunnel running):
```bash
# Activate virtual environment
python test-connection.py
```
- [ ] Output shows: **"✓ CONNECTION SUCCESSFUL!"**
- [ ] Database version detected
- [ ] Current database matches
- [ ] Table count appears

**Troubleshooting if failed:**
- Check SSH tunnel is still running
- Check `.env` configuration is correct
- Restart SSH tunnel
- Check port is not conflicting (change LOCAL_PORT if needed)

## ☑️ Checklist Before Running Seeder

### Safety Checks
- [ ] **WARNING:** Script will **TRUNCATE all tables** in database!
- [ ] Sure you're running on the correct database (not production!)
- [ ] Database backed up if needed
- [ ] Database in use is development/staging database

### Final Verification
- [ ] SSH tunnel active and running
- [ ] `test-connection.py` succeeded
- [ ] Virtual environment active
- [ ] All files in `MATERI/` folder complete
- [ ] AWS credentials are correct (test S3 upload)

## ☑️ Running Seeder

### Execution
```bash
python main.py
```

### Monitoring Progress
Watch the script output:
- [ ] Truncate tables succeeded
- [ ] Insert courses succeeded
- [ ] Upload audio files to S3 succeeded
- [ ] Insert lessons succeeded
- [ ] Upload markdown files to S3 succeeded
- [ ] Insert materi succeeded
- [ ] Upload quiz files to S3 succeeded
- [ ] Insert quiz succeeded

### Post-Execution
- [ ] Script completed without errors
- [ ] Check database: courses, lessons, materi, quiz data exists
- [ ] Check S3: audio, markdown, and quiz files uploaded
- [ ] Test database query to verify data

## ☑️ Common Troubleshooting

### Error: "Connection refused"
- [ ] SSH tunnel still running?
- [ ] Port in `.env` matches LOCAL_PORT?
- [ ] RDS endpoint is correct?

### Error: "Permission denied (publickey)"
- [ ] PEM key path is correct?
- [ ] (Linux/Mac) PEM key permissions = 400?
- [ ] EC2 username matches?

### Error: "S3 upload failed"
- [ ] AWS credentials in `.env` are correct?
- [ ] Bucket name exists and matches?
- [ ] IAM user has S3 permissions?

### Error: "Port already in use"
- [ ] Change LOCAL_PORT to another port (e.g.: 5433)
- [ ] Update LINGULU_DB_PORT in `.env` accordingly
- [ ] Restart SSH tunnel

---

## Summary Status

Use this checklist for tracking progress:

```
[ ] 1. AWS Resources Ready
[ ] 2. Security Groups Configured
[ ] 3. Python Environment Setup
[ ] 4. Environment Variables Configured
[ ] 5. SSH Access Verified
[ ] 6. Database Connection Tested
[ ] 7. SSH Tunnel Running
[ ] 8. test-connection.py PASSED
[ ] 9. Data Files Complete
[ ] 10. READY TO RUN SEEDER ✓
```

**If all checklists above are completed, you're ready to run:**
```bash
python main.py
```

---

**Last Updated:** February 28, 2026  
**Project:** Lingulu Data Seeder
