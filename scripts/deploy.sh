#!/bin/bash
set -e

APP_DIR="/opt/isc-security-bot"

echo "Deploying to $APP_DIR..."
cd $APP_DIR
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart isc-bot
echo "Deployment successful."
