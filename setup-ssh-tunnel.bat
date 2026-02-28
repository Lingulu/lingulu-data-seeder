@echo off
REM SSH Tunnel Setup Script for Lingulu Data Seeder (Windows Batch)
REM 
REM USAGE:
REM 1. Edit variables below according to your AWS configuration
REM 2. Double-click this file or run: setup-ssh-tunnel.bat
REM 3. Keep this terminal open while running the seeder
REM 4. Press Ctrl+C to stop the tunnel

REM ============================================
REM CONFIGURATION - EDIT THIS SECTION
REM ============================================

REM Path to PEM private key
set PEM_KEY_PATH=C:\Users\mario\.ssh\lingulu-ec2-key.pem

REM EC2 Configuration
set EC2_USER=ec2-user
set EC2_PUBLIC_IP=13.123.45.67

REM RDS Configuration
set RDS_ENDPOINT=lingulu-db.ch1234567890.ap-southeast-1.rds.amazonaws.com
set RDS_PORT=5432

REM Local Port for forwarding (use same port as .env LINGULU_DB_PORT)
set LOCAL_PORT=5432

REM ============================================
REM SCRIPT - DO NOT EDIT BELOW THIS LINE
REM ============================================

echo ================================================
echo   Lingulu Data Seeder - SSH Tunnel Setup
echo ================================================
echo.

REM Validate PEM key exists
if not exist "%PEM_KEY_PATH%" (
    echo [ERROR] PEM key not found: %PEM_KEY_PATH%
    echo Make sure the PEM key path is correct.
    pause
    exit /b 1
)

echo [INFO] Configuration:
echo   - PEM Key: %PEM_KEY_PATH%
echo   - EC2: %EC2_USER%@%EC2_PUBLIC_IP%
echo   - RDS: %RDS_ENDPOINT%:%RDS_PORT%
echo   - Local Port: %LOCAL_PORT%
echo.

echo [INFO] Starting SSH tunnel...
echo [INFO] Press Ctrl+C to stop the tunnel
echo.

REM Run SSH tunnel
ssh -i "%PEM_KEY_PATH%" -L %LOCAL_PORT%:%RDS_ENDPOINT%:%RDS_PORT% %EC2_USER%@%EC2_PUBLIC_IP% -N

if errorlevel 1 (
    echo.
    echo [ERROR] SSH tunnel failed
    echo.
    echo Troubleshooting:
    echo   1. Make sure EC2 instance is running
    echo   2. Check EC2 Security Group allows SSH ^(port 22^) from your IP
    echo   3. Verify PEM key and EC2 username are correct
    echo   4. Make sure port %LOCAL_PORT% is not already in use
    pause
    exit /b 1
)
