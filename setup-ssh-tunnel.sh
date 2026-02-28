#!/bin/bash

# SSH Tunnel Setup Script for Lingulu Data Seeder
# 
# USAGE:
# 1. Edit variables below according to your AWS configuration
# 2. Give execute permission: chmod +x setup-ssh-tunnel.sh
# 3. Run script: ./setup-ssh-tunnel.sh
# 4. Keep this terminal open while running the seeder
# 5. Press Ctrl+C to stop the tunnel

# ============================================
# CONFIGURATION - EDIT THIS SECTION
# ============================================

# Path to PEM private key
PEM_KEY_PATH="$HOME/.ssh/lingulu-ec2-key.pem"

# EC2 Configuration
EC2_USER="ec2-user"  # or ubuntu, admin, etc.
EC2_PUBLIC_IP="13.123.45.67"  # Replace with your EC2 public IP

# RDS Configuration
RDS_ENDPOINT="lingulu-db.ch1234567890.ap-southeast-1.rds.amazonaws.com"
RDS_PORT="5432"

# Local Port for forwarding (use same port as .env LINGULU_DB_PORT)
LOCAL_PORT="5432"

# ============================================
# SCRIPT - DO NOT EDIT BELOW THIS LINE
# ============================================

echo "================================================"
echo "  Lingulu Data Seeder - SSH Tunnel Setup"
echo "================================================"
echo ""

# Validate PEM key exists
if [ ! -f "$PEM_KEY_PATH" ]; then
    echo "[ERROR] PEM key not found: $PEM_KEY_PATH"
    echo "Make sure the PEM key path is correct."
    exit 1
fi

# Validate PEM key permissions
PEM_PERMS=$(stat -c %a "$PEM_KEY_PATH" 2>/dev/null || stat -f %A "$PEM_KEY_PATH" 2>/dev/null)
if [ "$PEM_PERMS" != "400" ] && [ "$PEM_PERMS" != "600" ]; then
    echo "[WARNING] PEM key permissions not secure: $PEM_PERMS"
    echo "[INFO] Setting permissions to 400..."
    chmod 400 "$PEM_KEY_PATH"
fi

echo "[INFO] Configuration:"
echo "  - PEM Key: $PEM_KEY_PATH"
echo "  - EC2: $EC2_USER@$EC2_PUBLIC_IP"
echo "  - RDS: $RDS_ENDPOINT:$RDS_PORT"
echo "  - Local Port: $LOCAL_PORT"
echo ""

echo "[INFO] Starting SSH tunnel..."
echo "[INFO] Press Ctrl+C to stop the tunnel"
echo ""

# Run SSH tunnel
ssh -i "$PEM_KEY_PATH" -L ${LOCAL_PORT}:${RDS_ENDPOINT}:${RDS_PORT} ${EC2_USER}@${EC2_PUBLIC_IP} -N

# If SSH fails
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] SSH tunnel failed"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Make sure EC2 instance is running"
    echo "  2. Check EC2 Security Group allows SSH (port 22) from your IP"
    echo "  3. Verify PEM key and EC2 username are correct"
    echo "  4. Make sure port $LOCAL_PORT is not already in use"
    exit 1
fi
