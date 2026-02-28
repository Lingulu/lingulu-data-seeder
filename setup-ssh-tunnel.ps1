# SSH Tunnel Setup Script for Lingulu Data Seeder
# 
# USAGE:
# 1. Edit variables below according to your AWS configuration
# 2. Run script: .\setup-ssh-tunnel.ps1
# 3. Keep this terminal open while running the seeder
# 4. Press Ctrl+C to stop the tunnel

# ============================================
# CONFIGURATION - EDIT THIS SECTION
# ============================================

# Path to PEM private key
$PEM_KEY_PATH = "C:\Users\mario\.ssh\lingulu-ec2-key.pem"

# EC2 Configuration
$EC2_USER = "ec2-user"  # or ubuntu, admin, etc.
$EC2_PUBLIC_IP = "13.123.45.67"  # Replace with your EC2 public IP

# RDS Configuration
$RDS_ENDPOINT = "lingulu-db.ch1234567890.ap-southeast-1.rds.amazonaws.com"
$RDS_PORT = "5432"

# Local Port for forwarding (use same port as .env LINGULU_DB_PORT)
$LOCAL_PORT = "5432"

# ============================================
# SCRIPT - DO NOT EDIT BELOW THIS LINE
# ============================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Lingulu Data Seeder - SSH Tunnel Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Validate PEM key exists
if (-not (Test-Path $PEM_KEY_PATH)) {
    Write-Host "[ERROR] PEM key not found: $PEM_KEY_PATH" -ForegroundColor Red
    Write-Host "Make sure the PEM key path is correct." -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Configuration:" -ForegroundColor Green
Write-Host "  - PEM Key: $PEM_KEY_PATH" -ForegroundColor White
Write-Host "  - EC2: $EC2_USER@$EC2_PUBLIC_IP" -ForegroundColor White
Write-Host "  - RDS: $RDS_ENDPOINT:$RDS_PORT" -ForegroundColor White
Write-Host "  - Local Port: $LOCAL_PORT" -ForegroundColor White
Write-Host ""

Write-Host "[INFO] Starting SSH tunnel..." -ForegroundColor Green
Write-Host "[INFO] Press Ctrl+C to stop the tunnel" -ForegroundColor Yellow
Write-Host ""

# Run SSH tunnel
$sshCommand = "ssh -i `"$PEM_KEY_PATH`" -L ${LOCAL_PORT}:${RDS_ENDPOINT}:${RDS_PORT} ${EC2_USER}@${EC2_PUBLIC_IP} -N"

try {
    Invoke-Expression $sshCommand
} catch {
    Write-Host ""
    Write-Host "[ERROR] SSH tunnel failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Make sure EC2 instance is running" -ForegroundColor White
    Write-Host "  2. Check EC2 Security Group allows SSH (port 22) from your IP" -ForegroundColor White
    Write-Host "  3. Verify PEM key and EC2 username are correct" -ForegroundColor White
    Write-Host "  4. Make sure port $LOCAL_PORT is not already in use" -ForegroundColor White
    exit 1
}
