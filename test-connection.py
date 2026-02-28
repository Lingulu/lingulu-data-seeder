#!/usr/bin/env python3
"""
Script to test database connection before running the seeder.
Use this script to verify that SSH tunnel and database configuration are correct.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

# Database configuration from .env
DB_CONFIG = {
    "host": os.getenv("LINGULU_DB_HOST", "localhost"),
    "port": int(os.getenv("LINGULU_DB_PORT", 5432)),
    "user": os.getenv("LINGULU_DB_USER", "postgres"),
    "password": os.getenv("LINGULU_DB_PASSWORD", "postgres"),
    "dbname": os.getenv("LINGULU_DB_NAME", "postgres"),
}

def test_connection():
    """Test database connection"""
    print("=" * 60)
    print("LINGULU DATA SEEDER - DATABASE CONNECTION TEST")
    print("=" * 60)
    print()
    
    print("[INFO] Database Configuration:")
    print(f"  - Host: {DB_CONFIG['host']}")
    print(f"  - Port: {DB_CONFIG['port']}")
    print(f"  - User: {DB_CONFIG['user']}")
    print(f"  - Database: {DB_CONFIG['dbname']}")
    print()
    
    print("[INFO] Attempting to connect to database...")
    
    try:
        # Attempt connection
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        
        cursor.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()
        
        # Success
        print()
        print("=" * 60)
        print("✓ CONNECTION SUCCESSFUL!")
        print("=" * 60)
        print()
        print("[INFO] Database Information:")
        print(f"  - Version: {db_version[0][:50]}...")
        print(f"  - Current Database: {current_db[0]}")
        print(f"  - Public Tables: {table_count[0]}")
        print()
        print("[SUCCESS] Database is ready to use!")
        print("[INFO] You can now run: python main.py")
        print()
        
        cursor.close()
        connection.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print()
        print("=" * 60)
        print("✗ CONNECTION FAILED!")
        print("=" * 60)
        print()
        print(f"[ERROR] {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Make sure SSH tunnel is running")
        print("     - Windows: .\\setup-ssh-tunnel.ps1")
        print("     - Linux/Mac: ./setup-ssh-tunnel.sh")
        print()
        print("  2. Verify configuration in .env file:")
        print("     - LINGULU_DB_HOST (localhost if using SSH tunnel)")
        print("     - LINGULU_DB_PORT")
        print("     - LINGULU_DB_USER")
        print("     - LINGULU_DB_PASSWORD")
        print("     - LINGULU_DB_NAME")
        print()
        print("  3. Check RDS Security Group allows access from EC2")
        print()
        print("  4. Test SSH tunnel manually:")
        print("     ssh -i path/to/key.pem ec2-user@ec2-ip")
        print()
        
        return False
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR!")
        print("=" * 60)
        print()
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        print()
        
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
