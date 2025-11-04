# 502 Bad Gateway - Quick Fix Summary

## What Was Wrong?
Your Flask app wasn't binding to the correct port that Render provides. Render assigns a dynamic port via the `PORT` environment variable, but your app was hardcoded to port 5000.

## What Was Fixed?

### 1. Procfile (Updated)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
```
- Binds to Render's dynamic PORT
- Uses 2 workers for better performance
- 120-second timeout for slow operations
- Info-level logging for debugging

### 2. app.py (Updated)
```python
# Get port from environment variable (required for Render)
port = int(os.getenv('PORT', 5000))
app.run(debug=debug_mode, host='0.0.0.0', port=port)
```
- Reads PORT from environment
- Falls back to 5000 for local development
- Uses environment-based debug mode

## Next Steps (CRITICAL!)

### 1. Set Environment Variables in Render
**Go to your Render dashboard → Environment tab:**

```
MONGO_URI=mongodb+srv://majorproject:Ys2DyC7cRkGo7zCv@cluster0.pra6fv6.mongodb.net/yogic_guide?retryWrites=true&w=majority&appName=Cluster0

SECRET_KEY=your-secure-random-key-here

FLASK_ENV=production

FLASK_DEBUG=False
```

### 2. MongoDB Atlas Network Access
1. Go to MongoDB Atlas dashboard
2. Network Access → Add IP Address
3. Add: `0.0.0.0/0` (allow all)
4. Save

### 3. Deploy
```bash
git add .
git commit -m "Fix: Port binding for Render"
git push origin main
```

Render will auto-deploy. Watch the logs!

## Test Your Deployment

```bash
# Health check
curl https://yogicguide.onrender.com/health

# Expected response:
# {"status":"healthy","timestamp":"...","database":"connected"}
```

## If Still Not Working

Check Render logs for:
- "MongoDB Atlas connected successfully!" ✅
- "Your service is live" ✅

If you see errors:
1. Verify MONGO_URI is set in Render (not just .env file)
2. Check MongoDB Atlas allows connections from 0.0.0.0/0
3. Ensure all environment variables are set

---

**That's it!** Your 502 error should be resolved after these changes are deployed.
