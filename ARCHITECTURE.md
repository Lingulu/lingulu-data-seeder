# Lingulu Data Seeder Connection Architecture

## SSH Tunnel Connection Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LINGULU DATA SEEDER                              │
│                        SSH Tunneling Architecture                        │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐                    ┌──────────────────┐                    ┌──────────────────┐
│                  │                    │                  │                    │                  │
│  Local Machine   │                    │  EC2 Instance    │                    │  RDS PostgreSQL  │
│                  │                    │                  │                    │                  │
│  ┌────────────┐  │                    │  ┌────────────┐  │                    │  ┌────────────┐  │
│  │            │  │   SSH Tunnel       │  │            │  │   Private Network  │  │            │  │
│  │   Python   │──┼───────────────────▶│  │  SSH       │──┼───────────────────▶│  │ Database   │  │
│  │   Script   │  │   Port 22          │  │  Server    │  │   Port 5432        │  │            │  │
│  │            │  │   (PEM Key Auth)   │  │            │  │   (Security Group) │  │            │  │
│  └────────────┘  │                    │  └────────────┘  │                    │  └────────────┘  │
│                  │                    │                  │                    │                  │
│  localhost:5432  │◀═══════════════════│  Port Forward    │                    │  RDS Endpoint    │
│                  │  Local Port        │                  │                    │  :5432           │
│                  │  Forwarding        │                  │                    │                  │
└──────────────────┘                    └──────────────────┘                    └──────────────────┘
       │                                        │                                        │
       │                                        │                                        │
       └────────────────┬───────────────────────┴────────────────────────────────────────┘
                        │
                        ▼
                  ┌──────────────────┐
                  │   AWS S3 Bucket  │
                  │                  │
                  │  lingulu-course  │
                  │                  │
                  │  (Upload Files)  │
                  └──────────────────┘
```

## Components

### 1. Local Machine
- **Function:** Run seeder script
- **Tools:** 
  - Python 3.x with dependencies
  - SSH client
  - AWS credentials for S3
- **Connection:** 
  - localhost:5432 → forwarded to RDS
  - HTTPS to S3 for file uploads

### 2. EC2 Instance
- **Function:** Gateway for private RDS access
- **Requirements:**
  - SSH Server running (port 22)
  - Network access to RDS (private subnet)
  - PEM private key for authentication
- **Security Group:**
  - Inbound: SSH (22) from your public IP
  - Outbound: PostgreSQL (5432) to RDS security group

### 3. RDS PostgreSQL
- **Function:** Database to store seeder data
- **Access:** Private (no public IP)
- **Security Group:**
  - Inbound: PostgreSQL (5432) from EC2 security group
  - Outbound: Default (all traffic)

### 4. AWS S3
- **Function:** Storage for audio and markdown files
- **Access:** Public via HTTPS
- **Bucket:** lingulu-course
- **Authentication:** AWS credentials (Access Key + Secret Key)

## Connection Flow

### A. SSH Tunnel Setup
```
1. Local Machine → EC2 Instance
   - Protocol: SSH
   - Port: 22
   - Auth: PEM private key
   - Command: ssh -i key.pem -L 5432:RDS_ENDPOINT:5432 ec2-user@EC2_IP -N

2. Local Port Binding
   - localhost:5432 → mapped to RDS via EC2
```

### B. Database Connection
```
1. Python script connects to localhost:5432
2. SSH tunnel forwards to EC2
3. EC2 forwards to RDS:5432 (private network)
4. Connection established ✓
```

### C. File Upload
```
1. Python script reads files from MATERI/
2. boto3 uploads to S3 bucket
3. S3 returns public URL
4. URL saved to database
```

## Security Layers

1. **SSH Authentication**
   - PEM private key (asymmetric encryption)
   - No password-based auth

2. **Network Isolation**
   - RDS in private subnet (no public access)
   - Security groups whitelist only EC2

3. **Database Authentication**
   - Username + password
   - Connection only via SSH tunnel

4. **S3 Access**
   - IAM credentials (Access Key + Secret)
   - Encrypted in transit (HTTPS)

## Troubleshooting Flow

```
┌─────────────────────────────────────────┐
│  Run: python test-connection.py         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Success?      │
         └────┬──────┬────┘
              │      │
         Yes  │      │ No
              │      │
              ▼      ▼
    ┌─────────────┐ ┌──────────────────────────┐
    │ Run seeder  │ │ Check SSH tunnel         │
    │ python      │ │ Is it running?           │
    │ main.py     │ └──────────┬───────────────┘
    └─────────────┘            │
                               ▼
                    ┌──────────────────────────┐
                    │ Check .env configuration │
                    │ - DB_HOST=localhost      │
                    │ - DB_PORT=5432           │
                    │ - DB_USER, PASSWORD, etc │
                    └──────────┬───────────────┘
                               │
                               ▼
                    ┌──────────────────────────┐
                    │ Check Security Groups    │
                    │ - EC2 allows SSH         │
                    │ - RDS allows EC2         │
                    └──────────────────────────┘
```

---

**Created:** February 28, 2026  
**Project:** Lingulu Data Seeder  
**Purpose:** Documentation for using SSH tunneling to access private RDS
