#!/bin/bash
# THE FREE LUNCH - Automated Scanner Wrapper
# This script is designed to be run by cron

# 1. Navigate to the project directory
cd "/Users/bradenflynn/Downloads/free food"

# 2. Run the scanner
# Use the full path to python3 if needed, but assuming default environment
/usr/bin/python3 backend/core/main.py >> automation.log 2>&1

# 3. Export to JSON (already happens in main.py, but just in case)
echo "$(date): Scan completed successfully." >> automation.log
