# Deploy Django Quiz App on AWS EC2 + Existing MySQL RDS (Option A)

This guide assumes:
- You already have an EC2 instance running (with Nginx for your other project).
- You already have a MySQL RDS instance running (currently used by your Spring project).
- You want to deploy this Django app on the same EC2 and same RDS instance, but **with a separate database**.

## 1) Create a separate database on the same RDS instance

Connect to RDS:

```bash
mysql -h <RDS_ENDPOINT> -u <USER> -p
```

Create a new DB for this app:

```sql
CREATE DATABASE quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON quiz_db.* TO '<USER>'@'%';
FLUSH PRIVILEGES;
EXIT;
```

## 2) Security Group check

Make sure RDS inbound rules allow MySQL (3306) **from your EC2 security group**.

## 3) Upload / clone code to EC2

Example:

```bash
cd /opt
sudo git clone https://github.com/<your-username>/<repo-name>.git quiz-app
sudo chown -R ubuntu:ubuntu /opt/quiz-app
cd /opt/quiz-app
```

## 4) Create venv and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5) Set environment variables for MySQL RDS

Set these in your shell for first-time setup:

```bash
export DJANGO_SECRET_KEY="change-me"
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="quiz.yourdomain.com,localhost"
export DJANGO_CSRF_TRUSTED_ORIGINS="https://quiz.yourdomain.com"

export DB_ENGINE=mysql
export MYSQL_HOST="<RDS_ENDPOINT>"
export MYSQL_PORT=3306
export MYSQL_DB=quiz_db
export MYSQL_USER="<USER>"
export MYSQL_PASSWORD="<PASSWORD>"
```

## 6) Migrate DB + create superuser + collect static

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 7) Run gunicorn on a separate port (example 8001)

```bash
gunicorn quiz_project.wsgi:application --bind 127.0.0.1:8001
```

## 8) systemd service for gunicorn (recommended)

Create:
`/etc/systemd/system/gunicorn_quiz.service`

```ini
[Unit]
Description=Gunicorn for Lunovian Quiz app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/opt/quiz-app
Environment="DJANGO_SECRET_KEY=change-me"
Environment="DJANGO_DEBUG=False"
Environment="DJANGO_ALLOWED_HOSTS=quiz.yourdomain.com,localhost"
Environment="DJANGO_CSRF_TRUSTED_ORIGINS=https://quiz.yourdomain.com"
Environment="DB_ENGINE=mysql"
Environment="MYSQL_HOST=<RDS_ENDPOINT>"
Environment="MYSQL_PORT=3306"
Environment="MYSQL_DB=quiz_db"
Environment="MYSQL_USER=<USER>"
Environment="MYSQL_PASSWORD=<PASSWORD>"
ExecStart=/opt/quiz-app/venv/bin/gunicorn quiz_project.wsgi:application --bind 127.0.0.1:8001

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_quiz
sudo systemctl start gunicorn_quiz
sudo systemctl status gunicorn_quiz
```

## 9) Nginx config (new domain / subdomain)

Create:
`/etc/nginx/sites-available/quiz`

```nginx
server {
    listen 80;
    server_name quiz.yourdomain.com;

    location /static/ {
        alias /opt/quiz-app/staticfiles/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8001;
    }
}
```

Enable + reload:

```bash
sudo ln -s /etc/nginx/sites-available/quiz /etc/nginx/sites-enabled/quiz
sudo nginx -t
sudo systemctl reload nginx
```

## 10) Optional HTTPS (recommended)

Use Certbot:

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d quiz.yourdomain.com
```

After HTTPS is enabled, keep:
`DJANGO_DEBUG=False`
and set:
`DJANGO_CSRF_TRUSTED_ORIGINS=https://quiz.yourdomain.com`


