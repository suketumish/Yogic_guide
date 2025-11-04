# Render Deployment Checklist

## ✅ Pre-Deployment (Completed)
- [x] Fixed port binding in `app.py` to use `PORT` environment variable
- [x] Updated `Procfile` with production Gunicorn configuration
- [x] Verified error templates exist (404.html, 500.html)
- [x] Health check endpoint available at `/health`

## 🔧 Render Dashboard Configuration

### 1. Environment Variables (CRITICAL)
Go to your Render service → Environment tab and add:

```
MONGO_URI=mongodb+srv://majorproject:Ys2DyC7cRkGo7zCv@cluster0.pra6fv6.mongodb.net/yogic_guide?retryWrites=true&w=majority&appName=Cluster0

SECRET_KEY=<generate-a-secure-random-key>

FLASK_ENV=production

FLASK_DEBUG=False
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: (leave empty - uses Procfile)
- **Python Version**: Detected from `runtime.txt` (3.11.9)

### 3. MongoDB Atlas Network Access
1. Login to MongoDB Atlas
2. Go to Network Access
3. Add IP Address: `0.0.0.0/0` (allows all) OR add Render's specific IPs
4. Save changes

## 🚀 Deployment Steps

1. **Commit Changes**:
   ```bash
   git add Procfile app.py
   git commit -m "Fix: Port binding for Render deployment"
   git push origin main
   ```

2. **Monitor Render Deployment**:
   - Go to Render dashboard
   - Watch the deployment logs
   - Look for "✅ MongoDB Atlas connected successfully!"
   - Wait for "Your service is live 🎉"

3. **Test Deployment**:
   ```bash
   # Health check
   curl https://yogicguide.onrender.com/health
   
   # Should return:
   # {"status":"healthy","timestamp":"...","database":"connected"}
   ```

4. **Visit Your Site**:
   - https://yogicguide.onrender.com/

## 🔍 Troubleshooting

### If you still see 502 error:

1. **Check Render Logs**:
   - Click on "Logs" tab in Render dashboard
   - Look for error messages during startup

2. **Common Errors**:

   **"MongoDB connection failed"**
   - ✅ Verify MONGO_URI is set in Render (not just .env)
   - ✅ Check MongoDB Atlas network access
   - ✅ Verify database credentials

   **"Address already in use"**
   - ✅ Fixed by using $PORT variable in Procfile

   **"Worker timeout"**
   - ✅ Fixed by setting --timeout 120 in Procfile

   **"Module not found"**
   - ✅ Check requirements.txt has all dependencies
   - ✅ Rebuild the service

3. **Test MongoDB Connection**:
   ```python
   # Run this locally to test your MongoDB URI
   from pymongo import MongoClient
   from pymongo.server_api import ServerApi
   
   uri = "mongodb+srv://majorproject:Ys2DyC7cRkGo7zCv@cluster0.pra6fv6.mongodb.net/yogic_guide?retryWrites=true&w=majority&appName=Cluster0"
   client = MongoClient(uri, server_api=ServerApi('1'))
   client.admin.command('ping')
   print("✅ MongoDB connected!")
   ```

## 📊 Post-Deployment Verification

- [ ] Home page loads: https://yogicguide.onrender.com/
- [ ] Health check works: https://yogicguide.onrender.com/health
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Admin login works: https://yogicguide.onrender.com/admin/login
  - Email: admin@yogicguide.com
  - Password: admin123

## 🔒 Security (Do This ASAP!)

1. **Change Admin Password**:
   - Login to admin panel
   - Change default password from `admin123`

2. **Secure SECRET_KEY**:
   - Generate new key (see above)
   - Update in Render environment variables

3. **Review MongoDB Access**:
   - Consider restricting to specific IPs if possible
   - Use strong database password

## 📝 Notes

- First deployment may take 2-3 minutes
- Render free tier may spin down after inactivity (takes ~30s to wake up)
- Check logs regularly for any issues
- Monitor MongoDB Atlas usage

---

**Need Help?**
- Render Docs: https://render.com/docs
- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/
- Check your Render service logs for specific errors
