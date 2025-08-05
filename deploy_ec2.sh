#!/bin/bash

# EduRAG EC2 Deployment Script for Amazon Linux
echo "🚀 EduRAG EC2 Deployment Script"
echo "==============================="

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python 3.9 and pip
echo "🐍 Installing Python 3.9..."
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++

# Install Git if not present
echo "📥 Installing Git..."
sudo yum install -y git

# Create application directory
APP_DIR="/opt/edurag"
echo "📁 Creating application directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown ec2-user:ec2-user $APP_DIR

# Clone or copy application files (assuming files are already on the server)
cd $APP_DIR

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data docs uploads logs

# Set up environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your GEMINI_API_KEY"
    echo "   sudo nano $APP_DIR/.env"
fi

# Create systemd service file
echo "⚙️  Creating systemd service..."
sudo tee /etc/systemd/system/edurag.service > /dev/null <<EOF
[Unit]
Description=EduRAG Web Application
After=network.target

[Service]
Type=exec
User=ec2-user
Group=ec2-user
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=FLASK_ENV=production
Environment=PORT=5000
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile $APP_DIR/logs/access.log --error-logfile $APP_DIR/logs/error.log app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo "🔄 Enabling and starting EduRAG service..."
sudo systemctl daemon-reload
sudo systemctl enable edurag
sudo systemctl start edurag

# Install and configure nginx
echo "🌐 Installing and configuring Nginx..."
sudo yum install -y nginx

# Create nginx configuration
sudo tee /etc/nginx/conf.d/edurag.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
    }
    
    # Static files (if any)
    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Remove default nginx configuration
sudo rm -f /etc/nginx/nginx.conf.default

# Enable and start nginx
echo "🔄 Enabling and starting Nginx..."
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure firewall (if firewalld is running)
if sudo systemctl is-active --quiet firewalld; then
    echo "🔥 Configuring firewall..."
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
fi

# Create log rotation configuration
echo "📄 Setting up log rotation..."
sudo tee /etc/logrotate.d/edurag > /dev/null <<EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ec2-user ec2-user
    postrotate
        sudo systemctl reload edurag
    endscript
}
EOF

# Create management script
tee $APP_DIR/manage.sh > /dev/null <<'EOF'
#!/bin/bash

case "$1" in
    start)
        sudo systemctl start edurag nginx
        echo "✅ EduRAG services started"
        ;;
    stop)
        sudo systemctl stop edurag nginx
        echo "⏹️  EduRAG services stopped"
        ;;
    restart)
        sudo systemctl restart edurag nginx
        echo "🔄 EduRAG services restarted"
        ;;
    status)
        echo "EduRAG Service Status:"
        sudo systemctl status edurag --no-pager
        echo ""
        echo "Nginx Service Status:"
        sudo systemctl status nginx --no-pager
        ;;
    logs)
        echo "EduRAG Application Logs:"
        tail -n 50 /opt/edurag/logs/error.log
        ;;
    update)
        cd /opt/edurag
        source venv/bin/activate
        git pull
        pip install -r requirements.txt
        sudo systemctl restart edurag
        echo "✅ EduRAG updated and restarted"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|update}"
        exit 1
        ;;
esac
EOF

chmod +x $APP_DIR/manage.sh

# Show status
echo ""
echo "🎉 EduRAG deployment completed!"
echo "================================"
echo ""
echo "📍 Application Directory: $APP_DIR"
echo "🌐 Web Interface: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "📋 Next Steps:"
echo "1. Edit the .env file with your GEMINI_API_KEY:"
echo "   sudo nano $APP_DIR/.env"
echo ""
echo "2. Upload your PDF files to the data directory:"
echo "   $APP_DIR/data/"
echo ""
echo "3. Restart the service after adding API key:"
echo "   sudo systemctl restart edurag"
echo ""
echo "📊 Management Commands:"
echo "   $APP_DIR/manage.sh start    - Start services"
echo "   $APP_DIR/manage.sh stop     - Stop services"
echo "   $APP_DIR/manage.sh restart  - Restart services"
echo "   $APP_DIR/manage.sh status   - Check status"
echo "   $APP_DIR/manage.sh logs     - View logs"
echo "   $APP_DIR/manage.sh update   - Update application"
echo ""
echo "🔍 Service Status:"
sudo systemctl status edurag --no-pager -l
echo ""
sudo systemctl status nginx --no-pager -l