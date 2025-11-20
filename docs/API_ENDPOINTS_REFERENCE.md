# 🔌 Yogic Guide - API Endpoints Reference

## Authentication Endpoints

### POST /register
Register a new user account
**Body:** `{ email, password, name, age, mobile, gender, experience }`
**Response:** Redirects to dashboard on success

### POST /login
User login
**Body:** `{ email, password }`
**Response:** Session cookie, redirects to dashboard

### POST /admin/login
Admin login
**Body:** `{ email, password }`
**Response:** Session cookie, redirects to admin dashboard

### GET /logout
Logout current user
**Response:** Clears session, redirects to landing page

### POST /forgot-password
Request password reset
**Body:** `{ email }`
**Response:** Sends reset token via email

### POST /reset-password/<token>
Reset password with token
**Body:** `{ email, password, confirm_password }`
**Response:** Updates password, redirects to login

---

## User Endpoints

### GET /dashboard
User dashboard (requires auth)
**Response:** HTML page with user stats and recent sessions

### GET /profile
User profile page (requires auth)
**Query Params:** `module` (optional) - filter sessions by module
**Response:** HTML page with profile and session history

### GET /badge-showcase
Badge system showcase (requires auth)
**Response:** HTML page demonstrating all badge types

---

## Module Endpoints

### GET /module/<module_type>
Start a module session (requires auth)
**Params:** `module_type` - breathing, stretching, surya-namaskar, meditation, yoga
**Response:** HTML session page with pose detection

### GET /module/surya-namaskar/info
Surya Namaskar information page
**Response:** HTML page with module details

### GET /module/breathing/info
Breathing exercises information page
**Response:** HTML page with module details

### GET /module/stretching/info
Stretching routine information page
**Response:** HTML page with module details
