# Deployment Guide

## Production Deployment Options

### Option 1: Traditional Server (VPS/Dedicated)

#### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Root or sudo access
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

# Install Nginx
sudo apt install nginx -y

# Install Supervisor (process manager)
sudo apt install supervisor -y
```

#### Step 2: Application Setup
```bash
# Create application directory
sudo mkdir -p /var/www/yogic-guide
cd /var/www/yogic-guide

# Clone or upload your code
# git clone <your-repo> .
# Or use SCP/SFTP to upload files

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
```

**.env for Production:**
```bash
SECRET_KEY=<generate-strong-secret-key>
MONGO_URI=mongodb://localhost:27017/yogic_guide
FLASK_ENV=production
```

```bash
# Seed database
python seed_poses.py

# Set permissions
sudo chown -R www-data:www-data /var/www/yogic-guide
```

#### Step 3: Gunicorn Configuration
```bash
# Create Gunicorn config
nano /var/www/yogic-guide/gunicorn_config.py
```

**gunicorn_config.py:**
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
```

#### Step 4: Supervisor Configuration
```bash
sudo nano /etc/supervisor/conf.d/yogic-guide.conf
```

**/etc/supervisor/conf.d/yogic-guide.conf:**
```ini
[program:yogic-guide]
directory=/var/www/yogic-guide
command=/var/www/yogic-guide/venv/bin/gunicorn -c gunicorn_config.py app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/yogic-guide/err.log
stdout_logfile=/var/log/yogic-guide/out.log
```

```bash
# Create log directory
sudo mkdir -p /var/log/yogic-guide
sudo chown -R www-data:www-data /var/log/yogic-guide

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start yogic-guide
```

#### Step 5: Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/yogic-guide
```

**/etc/nginx/sites-available/yogic-guide:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static {
        alias /var/www/yogic-guide/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Max upload size
    client_max_body_size 10M;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/yogic-guide /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### Step 6: SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is set up automatically
# Test renewal
sudo certbot renew --dry-run
```

#### Step 7: Firewall Configuration
```bash
# Enable UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Option 2: Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "app:app"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - MONGO_URI=mongodb://mongo:27017/yogic_guide
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/var/www/static
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mongo-data:
```

#### Deploy with Docker
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Option 3: Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.9.16" > runtime.txt

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create yogic-guide

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Seed database
heroku run python seed_poses.py
```

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 yogic-guide

# Create environment
eb create yogic-guide-env

# Deploy
eb deploy

# Open application
eb open
```

#### Google Cloud Platform (App Engine)
```yaml
# app.yaml
runtime: python39

instance_class: F2

env_variables:
  SECRET_KEY: "your-secret-key"
  MONGO_URI: "your-mongodb-uri"

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto
```

```bash
# Deploy
gcloud app deploy
```

### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Select Python as runtime
3. Add MongoDB database
4. Set environment variables
5. Deploy automatically

## Production Checklist

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Enable HTTPS/SSL
- [ ] Set secure session cookies
- [ ] Add CSRF protection
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Enable firewall
- [ ] Regular security updates

### Performance
- [ ] Enable Gzip compression
- [ ] Set up CDN for static files
- [ ] Configure caching headers
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Monitor memory usage
- [ ] Set up load balancing (if needed)

### Monitoring
- [ ] Set up error logging
- [ ] Configure application monitoring
- [ ] Set up uptime monitoring
- [ ] Configure alerts
- [ ] Monitor database performance
- [ ] Track user analytics

### Backup
- [ ] Set up MongoDB backups
- [ ] Backup application code
- [ ] Backup environment variables
- [ ] Test restore procedures
- [ ] Document backup process

### Documentation
- [ ] Update README with production URL
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Create user guide

## Environment Variables

### Required
```bash
SECRET_KEY=<strong-random-key>
MONGO_URI=mongodb://localhost:27017/yogic_guide
```

### Optional
```bash
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=10485760  # 10MB
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

## Monitoring & Logging

### Application Logs
```bash
# View Gunicorn logs
tail -f /var/log/gunicorn/error.log
tail -f /var/log/gunicorn/access.log

# View application logs
tail -f /var/log/yogic-guide/out.log
tail -f /var/log/yogic-guide/err.log
```

### MongoDB Logs
```bash
# View MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log
```

### Nginx Logs
```bash
# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Maintenance

### Update Application
```bash
# Pull latest code
cd /var/www/yogic-guide
git pull

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Restart application
sudo supervisorctl restart yogic-guide
```

### Database Backup
```bash
# Backup MongoDB
mongodump --db yogic_guide --out /backup/$(date +%Y%m%d)

# Restore MongoDB
mongorestore --db yogic_guide /backup/20240101/yogic_guide
```

### SSL Certificate Renewal
```bash
# Renew Let's Encrypt certificate
sudo certbot renew

# Restart Nginx
sudo systemctl restart nginx
```

## Troubleshooting

### Application Won't Start
```bash
# Check supervisor status
sudo supervisorctl status yogic-guide

# View logs
sudo tail -f /var/log/yogic-guide/err.log

# Restart
sudo supervisorctl restart yogic-guide
```

### Database Connection Issues
```bash
# Check MongoDB status
sudo systemctl status mongod

# Restart MongoDB
sudo systemctl restart mongod

# Check connection
mongo --eval "db.adminCommand('ping')"
```

### High Memory Usage
```bash
# Check memory
free -h

# Check processes
top

# Restart application
sudo supervisorctl restart yogic-guide
```

## Performance Optimization

### Nginx Caching
```nginx
# Add to nginx config
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
}
```

### MongoDB Indexing
```javascript
// Create indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.sessions.createIndex({ user_id: 1, start_time: -1 })
db.user_progress.createIndex({ user_id: 1 }, { unique: true })
```

### Gunicorn Workers
```python
# Calculate optimal workers
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1
```

## Cost Estimation

### VPS Hosting (DigitalOcean/Linode)
- Basic Droplet: $5-10/month
- Domain: $10-15/year
- SSL: Free (Let's Encrypt)
- **Total: ~$60-120/year**

### Cloud Platform (Heroku)
- Hobby Dyno: $7/month
- MongoDB: $15/month
- **Total: ~$264/year**

### AWS/GCP
- Variable based on usage
- Estimate: $20-50/month
- **Total: ~$240-600/year**

## Support & Resources

- Flask Deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- MongoDB: https://docs.mongodb.com/manual/administration/
- Let's Encrypt: https://letsencrypt.org/docs/

---

**Deployment Status:** Ready for production ✅
**Recommended:** VPS with Nginx + Gunicorn
**Estimated Setup Time:** 2-3 hours
