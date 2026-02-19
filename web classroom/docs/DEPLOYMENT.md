# Online Classroom - Deployment Guide

## Quick Start

### Windows (Local Development)
```bash
# Run the setup script
setup.bat

# Start the server
start_server.bat
```

### Linux (Local or VPS)
```bash
# Make scripts executable
chmod +x setup.sh start_server.sh

# Run the setup script
./setup.sh

# Start the server
./start_server.sh
```

---

## Production Deployment (VPS/Cloud)

### Prerequisites
- Ubuntu 20.04+ / Debian 10+ / CentOS 8+ / RHEL 8+
- Root or sudo access
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

### Option 1: Using Gunicorn + Nginx (Recommended)

#### 1. Complete Initial Setup
```bash
./setup.sh
```

#### 2. Install Production Dependencies
```bash
source .venv/bin/activate
pip install gunicorn
```

#### 3. Create Gunicorn Service
Create `/etc/systemd/system/classroom.service`:
```ini
[Unit]
Description=Online Classroom Gunicorn/Daphne Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/web classroom/w_classroom
Environment="PATH=/path/to/web classroom/.venv/bin"
ExecStart=/path/to/web classroom/.venv/bin/daphne -b 0.0.0.0 -p 8000 w_classroom.asgi:application

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/web classroom` with your actual path.

#### 4. Install and Configure Nginx
```bash
sudo apt install nginx  # Ubuntu/Debian
# or
sudo yum install nginx  # CentOS/RHEL
```

Create `/etc/nginx/sites-available/classroom`:
```nginx
upstream classroom {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    client_max_body_size 10M;

    location /static/ {
        alias /path/to/web classroom/w_classroom/staticfiles/;
    }

    location /ws/ {
        proxy_pass http://classroom;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://classroom;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/classroom /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Collect Static Files
```bash
cd w_classroom
python manage.py collectstatic --noinput
```

#### 6. Start Services
```bash
sudo systemctl start classroom
sudo systemctl enable classroom
sudo systemctl status classroom
```

#### 7. Setup SSL with Let's Encrypt (Recommended)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Using Docker (Alternative)

#### 1. Create Dockerfile
Create `Dockerfile` in the root directory:
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY w_classroom /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && \
    daphne -b 0.0.0.0 -p 8000 w_classroom.asgi:application
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./w_classroom:/app
      - static_volume:/app/staticfiles
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=your-domain.com,localhost
    restart: unless-stopped

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/static
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - web
    restart: unless-stopped

volumes:
  static_volume:
```

#### 3. Build and Run
```bash
docker-compose up -d --build
```

---

## Security Considerations for Production

### 1. Update Django Settings
Edit `w_classroom/settings.py`:
```python
# Set to False in production
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Use secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set secret key from environment variable
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key-here')
```

### 2. Use Environment Variables
Create `.env` file (add to .gitignore):
```bash
DJANGO_SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 3. Setup Redis for Production Channel Layer
Install Redis:
```bash
sudo apt install redis-server
pip install channels-redis
```

Update `w_classroom/settings.py`:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### 4. Setup Firewall
```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## Monitoring and Maintenance

### View Logs
```bash
# Systemd service logs
sudo journalctl -u classroom -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
sudo systemctl restart classroom
sudo systemctl restart nginx
```

### Backup Database
```bash
cd w_classroom
python manage.py dumpdata > backup.json
```

### Update Application
```bash
cd /path/to/web\ classroom
git pull  # If using git
source .venv/bin/activate
pip install -r w_classroom/requirements.txt
cd w_classroom
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart classroom
```

---

## Troubleshooting

### WebSocket Connection Issues
- Ensure Nginx is properly configured for WebSocket proxying
- Check that Daphne is running on the correct port
- Verify firewall rules allow WebSocket connections

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Permission Issues
```bash
sudo chown -R www-data:www-data /path/to/web\ classroom
sudo chmod -R 755 /path/to/web\ classroom
```

---

## Support

For issues or questions:
- Check the logs first
- Ensure all dependencies are installed
- Verify configuration files are correct
- Check firewall and network settings
