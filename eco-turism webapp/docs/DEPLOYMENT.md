# Django Eco-Tourism Webapp - Linux VPS Deployment Guide

## Pre-deployment Checklist

### 1. Environment Configuration
Create a `.env` file in `django_wp/tureco/` directory (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` with your production settings:
- Generate a new `SECRET_KEY` (you can use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- Set `DEBUG=False`
- Update `ALLOWED_HOSTS` with your domain name(s) and/or IP address

### 2. Install System Dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx supervisor redis-server
```

### 3. Setup Python Environment
```bash
cd /path/to/eco-turism-webapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

### 4. Configure Django
```bash
cd django_wp/tureco
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

### 5. Create Media Directory
```bash
mkdir -p media
chmod 755 media
```

### 6. Configure Gunicorn
Create a Gunicorn systemd service file: `/etc/systemd/system/tureco.service`

```ini
[Unit]
Description=Tureco Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/eco-turism-webapp/django_wp/tureco
Environment="PATH=/path/to/eco-turism-webapp/venv/bin"
ExecStart=/path/to/eco-turism-webapp/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn/tureco.sock \
    tureco.wsgi:application

[Install]
WantedBy=multi-user.target
```

Create socket directory:
```bash
sudo mkdir -p /run/gunicorn
sudo chown www-data:www-data /run/gunicorn
```

### 7. Configure Nginx
Create Nginx configuration: `/etc/nginx/sites-available/tureco`

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /path/to/eco-turism-webapp/django_wp/tureco/staticfiles/;
    }

    location /media/ {
        alias /path/to/eco-turism-webapp/django_wp/tureco/media/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn/tureco.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/tureco /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Start Services
```bash
sudo systemctl enable tureco
sudo systemctl start tureco
sudo systemctl status tureco
```

### 9. File Permissions
Set proper permissions:
```bash
cd /path/to/eco-turism-webapp/django_wp/tureco
sudo chown -R www-data:www-data media staticfiles logs
sudo chmod -R 755 media staticfiles
sudo chmod -R 775 logs
```

### 10. Security (Optional but Recommended)
Install SSL certificate with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Important Notes

### File Path Compatibility
- All file paths now use forward slashes `/` which work on both Windows and Linux
- The hardcoded Windows backslash in `hotel_detail.html` has been fixed

### Static and Media Files
- **STATIC_ROOT**: `/path/to/tureco/staticfiles/` - Collected static files
- **MEDIA_ROOT**: `/path/to/tureco/media/` - User uploaded files
- **MEDIA_URL**: Changed from `/uploads/` to `/media/` for clarity

### Database
- Currently using SQLite (not ideal for production)
- Consider migrating to PostgreSQL for production:
  ```bash
  sudo apt install postgresql postgresql-contrib
  pip install psycopg2-binary
  ```
  Then update `.env` with database credentials

### Logging
- Logs are stored in `django_wp/tureco/logs/`
- Ensure the directory has write permissions for the web server user

### Redis (for django-realtime-logs)
- Make sure Redis is running:
  ```bash
  sudo systemctl enable redis-server
  sudo systemctl start redis-server
  ```

## Troubleshooting

### Check Gunicorn logs:
```bash
sudo journalctl -u tureco -f
```

### Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Check application logs:
```bash
tail -f /path/to/eco-turism-webapp/django_wp/tureco/logs/tureco.log
```

### Permission issues:
If you encounter permission errors, verify:
```bash
ls -la media/
ls -la staticfiles/
ls -la logs/
```

All should be owned by `www-data:www-data` or your web server user.

## Updating the Application

```bash
cd /path/to/eco-turism-webapp
source venv/bin/activate
git pull  # if using git
pip install -r requirement.txt
cd django_wp/tureco
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart tureco
```
