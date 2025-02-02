#!/bin/bash

# Navigate to the repository directory
cd /home/ec2-user/web-app-repo

# Pull the latest changes
git pull origin main

# Copy the updated web_app.html to the Nginx web root
sudo cp web_app.html /usr/share/nginx/html/  # For Amazon Linux
# OR
sudo cp web_app.html /var/www/html/          # For Ubuntu

# Restart Nginx to apply changes
sudo systemctl restart nginx

echo "Deployment complete!"