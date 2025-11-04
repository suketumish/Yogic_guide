# 502 Bad Gateway Fix for Render Deployment

## Issues Fixed

### 1. Port Binding Issue ✅
**Problem**: App was hardcoded to port 5000, but Render requires binding to the `PORT` environment variable.

**Solution**: Updated `app.py` to read port from environment:
```python
port = int(os.getenv('PORT', 5000))
app.run(debug=debug_mode, host='0.0.0.0', port=port)
```

### 2. Gunicorn Configuration ✅
**Problem**: Basic Procfile without proper production settings.

**Solution**: Updated `Procfile` with production-ready configuration:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
```

## Deployment Steps for Render

### Step 1: Verify Environment Variables
In your Render dashboard, ensure these environment variables are set:

**Required:**
- `MONGO_URI` - Your MongoDB Atlas connection string
- `SECRET_KEY` - A secure random string for Flask sessions

**Optional (but recommended):**
- `FLASK_DEBUG` - Set to `False` for production
- `FLASK_ENV` - Set to `production`

### Step 2: Check MongoDB Connection
Your MongoDB URI in `.env` is:
```
mongodb+srv://majorproject:Ys2DyC7cRkGo7zCv@cluster0.pra6fv6.mongodb.net/yogic_guide?retryWrites=true&w=majority&appName=Cluster0
```

**Important**: Make sure this is also set in Render's environment variables (not just `.env` file).

### Step 3: Verify Build Settings
In Render dashboard:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: (Leave empty - Procfile will be used automatically)
- **Python Version**: 3.11.9 (from runtime.txt)

### Step 4: Deploy
1. Commit and push these changes to your repository
2. Render will automatically detect the changes and redeploy
3. Monitor the deployment logs for any errors

## Troubleshooting

### Check Deployment Logs
In Render dashboard, look for:
1. **Build Logs**: Ensure all dependencies install successfully
2. **Runtime Logs**: Check for application startup errors

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError"
**Solution**: Ensure all dependencies are in `requirements.txt`

#### Issue: "MongoDB connection failed"
**Solution**: 
- Verify `MONGO_URI` is set in Render environment variables
- Check MongoDB Atlas network access allows Render's IP (or allow all: 0.0.0.0/0)
- Verify database user credentials are correct

#### Issue: "Application timeout"
**Solution**: 
- Increased timeout to 120 seconds in Procfile
- Check if MongoDB connection is slow (network access settings)

#### Issue: "Worker timeout"
**Solution**: 
- Using 2 workers in Procfile (adjust based on your plan)
- Ensure your Render plan has sufficient resources

### Health Check Endpoint
Your app includes a health check at: `https://yogicguide.onrender.com/health`

This will return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-05T...",
  "database": "connected"
}
```

Use this to verify your deployment is working.

## Testing After Deployment

1. **Visit the home page**: https://yogicguide.onrender.com/
2. **Check health endpoint**: https://yogicguide.onrender.com/health
3. **Try to register**: Create a test account
4. **Login**: Verify authentication works
5. **Admin login**: https://yogicguide.onrender.com/admin/login
   - Email: `admin@yogicguide.com`
   - Password: `admin123` (change this!)

## Security Recommendations

### Before Going Live:
1. **Change SECRET_KEY**: Generate a secure random key
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Change Admin Password**: Login and update the default admin password

3. **Update MongoDB Network Access**: 
   - In MongoDB Atlas, go to Network Access
   - Add Render's IP addresses or use 0.0.0.0/0 (less secure but easier)

4. **Set Environment Variables in Render**:
   - Never commit sensitive data to git
   - Use Render's environment variables for all secrets

## Next Steps

1. Push these changes to your repository
2. Render will auto-deploy
3. Monitor logs during deployment
4. Test the health endpoint
5. Verify the application is accessible

## Support

If you still see 502 errors after deployment:
1. Check Render logs for specific error messages
2. Verify MongoDB connection string is correct
3. Ensure all environment variables are set
4. Check MongoDB Atlas network access settings
5. Verify your Render plan has sufficient resources

---

**Changes Made:**
- ✅ Updated `Procfile` with production Gunicorn settings
- ✅ Modified `app.py` to use PORT environment variable
- ✅ Added proper error handling and logging
- ✅ Verified error templates exist (404.html, 500.html)
