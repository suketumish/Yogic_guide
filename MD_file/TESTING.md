# Testing Guide

## Manual Testing Checklist

### 1. User Authentication

#### Registration
- [ ] Navigate to `/register`
- [ ] Fill all required fields
- [ ] Submit form
- [ ] Verify redirect to login page
- [ ] Check MongoDB for new user entry

**Test Cases:**
```
Valid Registration:
- Name: John Doe
- Email: john@example.com
- Password: Test123!
- Age: 25
- Experience: Beginner

Invalid Cases:
- Duplicate email (should show error)
- Missing required fields (should show validation)
- Invalid email format (should show error)
```

#### Login
- [ ] Navigate to `/login`
- [ ] Enter valid credentials
- [ ] Verify redirect to dashboard
- [ ] Check session cookie is set
- [ ] Test "Remember Me" functionality

**Test Cases:**
```
Valid Login:
- Email: john@example.com
- Password: Test123!

Invalid Cases:
- Wrong password (should show error)
- Non-existent email (should show error)
- Empty fields (should show validation)
```

#### Logout
- [ ] Click logout button
- [ ] Verify redirect to login page
- [ ] Verify session is cleared
- [ ] Try accessing dashboard (should redirect to login)

### 2. Dashboard

#### Display
- [ ] User name displays correctly
- [ ] Total sessions count shows
- [ ] All 3 module cards visible
- [ ] Progress section displays stats
- [ ] Profile icon clickable

#### Navigation
- [ ] Click "Full Body Stretching" → redirects to session
- [ ] Click "Breathing Exercises" → redirects to breathing selection
- [ ] Click "Surya Namaskar" → redirects to session
- [ ] Click profile icon → redirects to profile page
- [ ] Click logout → logs out successfully

### 3. Profile Page

#### Display
- [ ] User details show correctly
- [ ] Recent sessions list displays
- [ ] Session history shows dates and durations
- [ ] Back to dashboard link works

#### Data Verification
- [ ] Check MongoDB for user data
- [ ] Verify session history matches database
- [ ] Test with user who has no sessions

### 4. Full Body Stretching Module

#### Session Start
- [ ] Camera permission requested
- [ ] Video feed displays
- [ ] Namaste gesture detection starts
- [ ] 5-second countdown works
- [ ] Audio instruction plays

#### Pose Detection
- [ ] Skeleton overlay appears
- [ ] Joints are marked correctly
- [ ] Lines connect joints properly
- [ ] Pose name displays
- [ ] Timer counts down

#### Pose Validation
- [ ] Green skeleton for correct pose
- [ ] Red skeleton for incorrect pose
- [ ] Screen blinks red on error
- [ ] Angle measurements display
- [ ] Feedback text updates

#### Pose Sequence
- [ ] Pose 1: Mountain Pose (20s)
- [ ] Pose 2: Forward Bend (25s)
- [ ] Pose 3: Warrior I (30s)
- [ ] Pose 4: Triangle Pose (25s)
- [ ] Pose 5: Child's Pose (30s)
- [ ] Progress bar updates
- [ ] Next pose preview shows

#### Audio Feedback
- [ ] Pose name announced
- [ ] Instructions narrated
- [ ] "Well done" after each pose
- [ ] No audio overlap

#### Controls
- [ ] Pause button works
- [ ] Resume functionality works
- [ ] Stop button shows confirmation
- [ ] Stop redirects to summary

### 5. Breathing Exercises Module

#### Exercise Selection
- [ ] 4 exercise cards display
- [ ] Click Anulom Vilom → starts exercise
- [ ] Click Bhramari → starts exercise
- [ ] Click Kapalbhati → starts exercise
- [ ] Click Meditation → starts exercise

#### Exercise Execution
- [ ] Seated position detection
- [ ] Timer displays correctly
- [ ] Audio instructions play
- [ ] Pause/Resume works
- [ ] Stop button works

### 6. Surya Namaskar Module

#### 12-Pose Sequence
- [ ] All 12 poses execute in order
- [ ] Each pose holds for 5 seconds
- [ ] Smooth transitions between poses
- [ ] Audio guidance for each pose
- [ ] Progress tracking works

#### Continuous Flow
- [ ] No interruptions between poses
- [ ] Timer resets for each pose
- [ ] Skeleton overlay updates
- [ ] Benefits/cautions update

### 7. Session Complete Page

#### Display
- [ ] Success message shows
- [ ] Duration displays correctly
- [ ] Poses completed count accurate
- [ ] Accuracy percentage shows
- [ ] Calories burned displays

#### Functionality
- [ ] Star rating clickable
- [ ] Back to dashboard works
- [ ] View profile works
- [ ] Share button works (if supported)

#### Data Persistence
- [ ] Check MongoDB sessions collection
- [ ] Verify session data saved
- [ ] Check user_progress updated
- [ ] Total sessions incremented

### 8. MediaPipe Integration

#### Pose Detection
- [ ] Landmarks detected correctly
- [ ] 33 points tracked
- [ ] Smooth tracking (no jitter)
- [ ] Works in different lighting
- [ ] Handles occlusion gracefully

#### Angle Calculation
- [ ] Elbow angles calculated
- [ ] Knee angles calculated
- [ ] Shoulder angles calculated
- [ ] Angles display in real-time
- [ ] Tolerance (±15°) works

### 9. Browser Compatibility

#### Chrome
- [ ] Camera access works
- [ ] MediaPipe loads
- [ ] Audio plays
- [ ] All features functional

#### Firefox
- [ ] Camera access works
- [ ] MediaPipe loads
- [ ] Audio plays
- [ ] All features functional

#### Edge
- [ ] Camera access works
- [ ] MediaPipe loads
- [ ] Audio plays
- [ ] All features functional

#### Safari (Limited)
- [ ] Camera access works
- [ ] MediaPipe loads (may be slow)
- [ ] Audio plays
- [ ] Note any issues

### 10. Responsive Design

#### Desktop (1920x1080)
- [ ] Layout looks good
- [ ] All elements visible
- [ ] No overflow issues

#### Laptop (1366x768)
- [ ] Layout adapts
- [ ] Camera feed sized correctly
- [ ] Side panel visible

#### Tablet (768x1024)
- [ ] Grid layout stacks
- [ ] Touch controls work
- [ ] Camera feed responsive

#### Mobile (375x667)
- [ ] Single column layout
- [ ] All features accessible
- [ ] Camera works on mobile

### 11. Error Handling

#### Camera Errors
- [ ] No camera detected → error message
- [ ] Permission denied → helpful message
- [ ] Camera in use → error message

#### Network Errors
- [ ] MongoDB connection lost → error
- [ ] Session save fails → retry option
- [ ] API timeout → error message

#### User Errors
- [ ] Invalid input → validation message
- [ ] Session timeout → redirect to login
- [ ] Duplicate registration → error

### 12. Performance

#### Load Times
- [ ] Dashboard loads < 2s
- [ ] Session page loads < 3s
- [ ] Camera initializes < 2s
- [ ] MediaPipe loads < 3s

#### Frame Rate
- [ ] Video feed smooth (30fps)
- [ ] Skeleton overlay smooth
- [ ] No lag during detection
- [ ] Responsive controls

#### Memory Usage
- [ ] No memory leaks
- [ ] Stable over long sessions
- [ ] Browser doesn't slow down

## Automated Testing (Future)

### Unit Tests
```python
# test_auth.py
def test_registration():
    # Test user registration
    pass

def test_login():
    # Test user login
    pass

def test_logout():
    # Test user logout
    pass
```

### Integration Tests
```python
# test_session.py
def test_session_creation():
    # Test session start
    pass

def test_session_completion():
    # Test session end
    pass
```

### API Tests
```python
# test_api.py
def test_pose_validation():
    # Test pose validation endpoint
    pass

def test_session_stats():
    # Test session stats endpoint
    pass
```

## Test Data

### Sample Users
```json
{
  "name": "Test User 1",
  "email": "test1@example.com",
  "password": "Test123!",
  "age": 25,
  "experience_level": "Beginner"
}

{
  "name": "Test User 2",
  "email": "test2@example.com",
  "password": "Test123!",
  "age": 35,
  "experience_level": "Intermediate"
}
```

### Sample Sessions
```json
{
  "module_type": "stretching",
  "duration": 150,
  "poses_completed": 5,
  "accuracy_score": 85,
  "calories_burned": 8
}
```

## Bug Reporting Template

```markdown
**Bug Title:** [Brief description]

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. See error

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshots:**
[If applicable]

**Environment:**
- Browser: Chrome 120
- OS: Windows 11
- Screen: 1920x1080

**Console Errors:**
[Any JavaScript errors]
```

## Performance Benchmarks

### Target Metrics
- Page load: < 3 seconds
- Camera init: < 2 seconds
- Pose detection: 30 FPS
- API response: < 500ms
- Database query: < 100ms

### Monitoring
```bash
# Check MongoDB performance
mongo
> use yogic_guide
> db.sessions.stats()

# Check Flask logs
tail -f app.log
```

## Security Testing

### Authentication
- [ ] Passwords are hashed (bcrypt)
- [ ] Sessions expire correctly
- [ ] No password in logs
- [ ] SQL injection prevented (using MongoDB)

### Authorization
- [ ] Users can only access own data
- [ ] Session validation works
- [ ] Logout clears session

### Input Validation
- [ ] Email format validated
- [ ] Age range validated
- [ ] XSS prevention
- [ ] CSRF protection (add tokens)

## Accessibility Testing

### Screen Reader
- [ ] All images have alt text
- [ ] Form labels present
- [ ] Navigation logical
- [ ] Errors announced

### Keyboard Navigation
- [ ] Tab order logical
- [ ] All buttons accessible
- [ ] Forms submittable
- [ ] Modals closable

### Color Contrast
- [ ] Text readable
- [ ] Buttons visible
- [ ] Error messages clear
- [ ] WCAG AA compliant

## Load Testing (Future)

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Using Locust
locust -f locustfile.py
```

## Continuous Integration (Future)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
```

---

**Testing Status:** Manual testing complete ✅
**Automated Tests:** To be implemented
**Coverage Goal:** 80%+
