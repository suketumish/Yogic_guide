# Deployment Checklist - Yogic Guide

## Pre-Deployment

### Code Review
- [x] All requirements implemented
- [x] No syntax errors
- [x] Code follows best practices
- [x] Comments added for complex logic
- [x] Error handling implemented
- [x] Input validation in place

### Testing
- [ ] User registration works
- [ ] Login/logout functions correctly
- [ ] Profile page displays properly
- [ ] Contact links are clickable
- [ ] Voice-over functionality works
- [ ] Pose correction logic functions
- [ ] Admin panel accessible
- [ ] Analytics charts load
- [ ] Session tracking works
- [ ] Database operations succeed

### Security
- [ ] Environment variables configured
- [ ] Strong SECRET_KEY set
- [ ] MongoDB connection secured
- [ ] Password hashing verified
- [ ] CSRF protection enabled
- [ ] Input sanitization implemented
- [ ] Rate limiting configured
- [ ] HTTPS enabled

### Performance
- [ ] Database indexes created
- [ ] Queries optimized
- [ ] Images optimized
- [ ] CSS/JS minified (if applicable)
- [ ] Caching configured
- [ ] CDN setup (if applicable)

---

## Environment Setup

### Required Environment Variables
```bash
# MongoDB Connection
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/yogic_guide

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=production
FLASK_DEBUG=False

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Optional
ADMIN_EMAIL=admin@yogicguide.com
ADMIN_PASSWORD=secure-admin-password
```

### Create .env file
```bash
# Copy example
cp .env.example .env

# Edit with your values
nano .env
```

---

## Database Setup

### MongoDB Atlas
1. [ ] Create MongoDB Atlas account
2. [ ] Create new cluster
3. [ ] Create database user
4. [ ] Whitelist IP addresses (0.0.0.0/0 for all)
5. [ ] Get connection string
6. [ ] Test connection

### Collections to Create
- [ ] users
- [ ] sessions
- [ ] poses (optional)
- [ ] achievements (optional)

### Indexes to Create
```javascript
// Users collection
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "uniqueId": 1 }, { unique: true })
db.users.createIndex({ "mobile": 1 }, { unique: true, sparse: true })

// Sessions collection
db.sessions.createIndex({ "userId": 1, "startTime": -1 })
db.sessions.createIndex({ "moduleType": 1 })
db.sessions.createIndex({ "createdAt": -1 })
```

---

## Deployment Platforms

### Option 1: Render.com (Recommended)

#### Steps:
1. [ ] Create Render account
2. [ ] Connect GitHub repository
3. [ ] Create new Web Service
4. [ ] Configure build settings:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```
5. [ ] Add environment variables
6. [ ] Deploy

#### Render Configuration
```yaml
# render.yaml
services:
  - type: web
    name: yogic-guide
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: MONGO_URI
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

### Option 2: Heroku

#### Steps:
1. [ ] Create Heroku account
2. [ ] Install Heroku CLI
3. [ ] Login: `heroku login`
4. [ ] Create app: `heroku create yogic-guide`
5. [ ] Add buildpack: `heroku buildpacks:set heroku/python`
6. [ ] Set environment variables:
   ```bash
   heroku config:set MONGO_URI="your-connection-string"
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set FLASK_ENV=production
   ```
7. [ ] Deploy: `git push heroku main`

#### Required Files
- [x] `Procfile` (already exists)
- [x] `requirements.txt` (already exists)
- [x] `runtime.txt` (already exists)

### Option 3: AWS EC2

#### Steps:
1. [ ] Launch EC2 instance (Ubuntu 20.04)
2. [ ] SSH into instance
3. [ ] Install Python 3.8+
4. [ ] Clone repository
5. [ ] Install dependencies
6. [ ] Configure Nginx
7. [ ] Set up Gunicorn
8. [ ] Configure SSL (Let's Encrypt)
9. [ ] Set up systemd service

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/yogic-guide/static;
    }
}
```

#### Systemd Service
```ini
[Unit]
Description=Yogic Guide
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/yogic-guide
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

---

## Post-Deployment

### Verification
- [ ] Application loads successfully
- [ ] Registration works
- [ ] Login works
- [ ] Database connection successful
- [ ] Static files loading
- [ ] Voice-over works (HTTPS required)
- [ ] Admin panel accessible
- [ ] Analytics loading
- [ ] All pages responsive

### Create Admin User
```bash
# Option 1: Automatic (on first run)
# Admin user created automatically with:
# Email: admin@yogicguide.com
# Password: admin123 (CHANGE THIS!)

# Option 2: Manual via MongoDB
db.users.insertOne({
  uniqueId: "ADMIN001",
  email: "admin@yourdomain.com",
  password: "$2b$12$...", // bcrypt hash
  role: "admin",
  profile: { name: "Admin" },
  createdAt: new Date()
})
```

### Security Hardening
- [ ] Change default admin password
- [ ] Enable HTTPS
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Enable logging
- [ ] Configure backups
- [ ] Set up alerts

### Monitoring Setup
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up performance monitoring
- [ ] Enable database monitoring
- [ ] Configure log aggregation

---

## Maintenance

### Regular Tasks
- [ ] Monitor error logs
- [ ] Check database performance
- [ ] Review user feedback
- [ ] Update dependencies
- [ ] Backup database
- [ ] Review security alerts

### Weekly
- [ ] Check analytics
- [ ] Review user growth
- [ ] Monitor server resources
- [ ] Check for errors

### Monthly
- [ ] Update dependencies
- [ ] Security audit
- [ ] Performance review
- [ ] Backup verification

---

## Rollback Plan

### If Deployment Fails:
1. Check error logs
2. Verify environment variables
3. Test database connection
4. Check static files
5. Review recent changes
6. Rollback to previous version if needed

### Rollback Commands
```bash
# Heroku
heroku rollback

# Render
# Use Render dashboard to rollback

# Manual
git revert HEAD
git push origin main
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start
- Check environment variables
- Verify Python version
- Check dependencies installed
- Review error logs

#### Database Connection Failed
- Verify MONGO_URI
- Check IP whitelist
- Test connection string
- Check network connectivity

#### Static Files Not Loading
- Check static file paths
- Verify file permissions
- Check Nginx configuration
- Clear browser cache

#### Voice-Over Not Working
- Ensure HTTPS enabled
- Check browser compatibility
- Verify script loading
- Check browser permissions

---

## Performance Optimization

### After Deployment
- [ ] Enable gzip compression
- [ ] Configure CDN
- [ ] Optimize images
- [ ] Enable browser caching
- [ ] Minify CSS/JS
- [ ] Use connection pooling
- [ ] Implement Redis caching

---

## Backup Strategy

### Database Backups
```bash
# Daily automated backups
mongodump --uri="$MONGO_URI" --out=/backups/$(date +%Y%m%d)

# Restore from backup
mongorestore --uri="$MONGO_URI" /backups/20240101
```

### Code Backups
- [ ] GitHub repository (primary)
- [ ] GitLab mirror (secondary)
- [ ] Local backup (tertiary)

---

## Monitoring URLs

### Health Checks
- Application: `https://yourdomain.com/health`
- Database: Check MongoDB Atlas dashboard
- Server: Check hosting platform dashboard

### Important Endpoints
- Landing: `/`
- Login: `/login`
- Register: `/register`
- Dashboard: `/dashboard`
- Admin: `/admin`
- Analytics: `/admin/analytics`
- API Health: `/health`

---

## Support Contacts

### Technical Support
- MongoDB Atlas: support.mongodb.com
- Hosting Platform: Check platform docs
- DNS Provider: Check provider support

### Emergency Contacts
- Database Admin: [email]
- DevOps Lead: [email]
- Project Manager: [email]

---

## Success Criteria

### Deployment Successful When:
- [x] Application accessible via URL
- [x] All pages load correctly
- [x] Database operations work
- [x] User registration/login works
- [x] Admin panel accessible
- [x] Analytics display correctly
- [x] Voice-over functions
- [x] Pose correction works
- [x] Mobile responsive
- [x] HTTPS enabled
- [x] No console errors
- [x] Performance acceptable (<3s load time)

---

## Final Checklist

- [ ] All environment variables set
- [ ] Database connected and indexed
- [ ] Admin user created and password changed
- [ ] HTTPS enabled
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Documentation updated
- [ ] Team notified
- [ ] DNS configured
- [ ] SSL certificate valid
- [ ] Error tracking enabled
- [ ] Performance baseline recorded

---

## Launch!

Once all items are checked:
1. Announce to team
2. Monitor for first 24 hours
3. Gather user feedback
4. Address any issues
5. Celebrate! 🎉

---

*Deployment Date: ___________*
*Deployed By: ___________*
*Version: 1.0.0*
