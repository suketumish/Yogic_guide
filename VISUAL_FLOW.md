# Visual Flow - Dashboard Module Details

## 📱 User Experience Flow

### Initial State (Dashboard Load)
```
┌─────────────────────────────────────────────────────────┐
│  🧘 YOGIC GUIDE                    👤 PROFILE  LOGOUT   │
└─────────────────────────────────────────────────────────┘

Welcome back, Saket Kumar! 🙏
Ready to continue your wellness journey?

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   🧘‍♀️            │  │      🌬️          │  │       ☀️          │
│ FULL BODY        │  │   BREATHING      │  │  SURYA NAMASKAR  │
│ STRETCHING       │  │   EXERCISES      │  │                  │
│                  │  │                  │  │                  │
│ ⏱ 15-20 min     │  │ ⏱ 10-15 min     │  │ ⏱ 10-12 min     │
│ 📊 Beginner     │  │ 📊 All Levels   │  │ 📊 Intermediate  │
│ 🔥 ~50 kcal     │  │ 🧘 Relaxation   │  │ 🔥 ~80 kcal     │
│                  │  │                  │  │                  │
│ [VIEW DETAILS ↓] │  │ [VIEW DETAILS ↓] │  │ [VIEW DETAILS ↓] │
└──────────────────┘  └──────────────────┘  └──────────────────┘

Your Progress
🎯 0 Sessions  🔥 0 Streak  ⏱️ 0 Minutes
```

---

### When User Clicks "VIEW DETAILS ↓" on Stretching
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   🧘‍♀️            │  │      🌬️          │  │       ☀️          │
│ FULL BODY        │  │   BREATHING      │  │  SURYA NAMASKAR  │
│ STRETCHING       │  │   EXERCISES      │  │                  │
│ [VIEW DETAILS ↓] │  │ [VIEW DETAILS ↓] │  │ [VIEW DETAILS ↓] │
└──────────────────┘  └──────────────────┘  └──────────────────┘

↓ EXPANDS WITH SMOOTH ANIMATION ↓

┌─────────────────────────────────────────────────────────┐
│  🧘‍♀️ Full Body Stretching Details              ✕       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✨ Benefits                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 💪       │  │ 🧘       │  │ 😌       │             │
│  │Improved  │  │ Better   │  │ Stress   │             │
│  │Flexibility│  │ Posture  │  │ Relief   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                          │
│  🧘 12 Stretching Poses                                 │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ ① Neck Rolls    │  │ ② Shoulder      │             │
│  │ 30 sec          │  │    Shrugs       │             │
│  └─────────────────┘  │ 10 reps         │             │
│                       └─────────────────┘             │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ ③ Arm Circles   │  │ ④ Side Bends    │             │
│  │ 20 circles      │  │ 30 sec/side     │             │
│  └─────────────────┘  └─────────────────┘             │
│                                                          │
│  ... (8 more poses) ...                                 │
│                                                          │
│           [START SESSION →]                             │
└─────────────────────────────────────────────────────────┘

↓ AUTO-SCROLLS TO THIS SECTION ↓
```

---

### When User Clicks "VIEW DETAILS ↓" on Breathing
```
┌─────────────────────────────────────────────────────────┐
│  🌬️ Breathing Exercises Details                ✕       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✨ Benefits of Pranayama                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 🧠       │  │ ❤️       │  │ 😌       │             │
│  │ Mental   │  │ Heart    │  │ Stress   │             │
│  │ Clarity  │  │ Health   │  │Reduction │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                          │
│  🌬️ 4 Pranayama Techniques                             │
│  ┌─────────────────────────────────────────────┐       │
│  │ 1️⃣ Anulom Vilom (Alternate Nostril)         │       │
│  │ Balances left and right brain hemispheres   │       │
│  │ ⏱ 3-5 min  Balance & Calm                   │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ 2️⃣ Kapalbhati (Skull Shining Breath)        │       │
│  │ Energizing breath that cleanses system      │       │
│  │ ⏱ 2-3 min  🔥 Energizing                    │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ 3️⃣ Bhramari (Bee Breath)                    │       │
│  │ Calming breath that reduces anxiety         │       │
│  │ ⏱ 2-3 min  😌 Calming                       │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ 4️⃣ Ujjayi (Ocean Breath)                    │       │
│  │ Victorious breath that builds heat          │       │
│  │ ⏱ 5-10 min  🎯 Focus                        │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│           [START SESSION →]                             │
└─────────────────────────────────────────────────────────┘
```

---

### When User Clicks "VIEW DETAILS ↓" on Surya Namaskar
```
┌─────────────────────────────────────────────────────────┐
│  ☀️ Surya Namaskar Details                      ✕       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────┐       │
│  │ ☀️ About Sun Salutation                     │       │
│  │ A sequence of 12 powerful yoga poses that   │       │
│  │ pay homage to the sun. Combines physical    │       │
│  │ exercise, breathing, and meditation.        │       │
│  └─────────────────────────────────────────────┘       │
│                                                          │
│  ✨ Benefits                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 💪       │  │ ❤️       │  │ 🔥       │             │
│  │Full Body │  │ Cardio   │  │ Boosts   │             │
│  │ Workout  │  │ Health   │  │Metabolism│             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                          │
│  🌞 The 12 Sacred Poses                                 │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ ① Pranamasana   │  │ ② Hasta         │             │
│  │ Prayer Pose     │  │   Uttanasana    │             │
│  │ Centering       │  │ Raised Arms     │             │
│  └─────────────────┘  └─────────────────┘             │
│                                                          │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ ③ Hasta         │  │ ④ Ashwa         │             │
│  │   Padasana      │  │   Sanchalanasana│             │
│  │ Hand to Foot    │  │ Equestrian      │             │
│  └─────────────────┘  └─────────────────┘             │
│                                                          │
│  ... (8 more poses) ...                                 │
│                                                          │
│           [START SESSION →]                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Themes

### Stretching Module
- **Primary**: Indigo/Blue (#4F46E5, #3B82F6)
- **Cards**: Light indigo/blue backgrounds
- **Badges**: Green numbered circles

### Breathing Module
- **Primary**: Blue/Purple (#3B82F6, #9333EA)
- **Cards**: Gradient backgrounds (blue→indigo, orange→red, purple→pink, teal→cyan)
- **Badges**: Color-coded by technique type

### Surya Namaskar Module
- **Primary**: Orange/Red (#FF9800, #FF6F00)
- **Cards**: Orange/yellow backgrounds
- **Badges**: Orange numbered circles (sun theme)

---

## 🎬 Animations

### Expand Animation
```
Initial: max-height: 0 (hidden)
         ↓
Click:   max-height: 5000px (smooth transition 0.8s)
         ↓
Result:  Content visible with smooth expansion
```

### Collapse Animation
```
Expanded: max-height: 5000px
          ↓
Click ✕:  max-height: 0 (smooth transition 0.5s)
          ↓
Result:   Content hidden with smooth collapse
```

### Hover Effects
- Cards lift up (translateY: -2px)
- Shadow increases
- Border color changes
- Smooth transition (0.3s)

---

## 📱 Mobile Responsive

### Desktop (>768px)
- 3 module cards in a row
- 2 pose cards per row in details
- Full width sections

### Tablet (768px)
- 2 module cards per row
- 2 pose cards per row
- Adjusted padding

### Mobile (<576px)
- 1 module card per row
- 1 pose card per row
- Compact spacing
- Touch-friendly buttons

---

## ✨ Key Features

1. **No Page Reload** - Everything on same page
2. **Smooth Animations** - Professional transitions
3. **Auto-Scroll** - Automatically scrolls to expanded section
4. **Close Button** - ✕ to collapse details
5. **Color-Coded** - Each module has unique theme
6. **Hover Effects** - Interactive card animations
7. **Mobile Friendly** - Responsive design
8. **Direct Action** - "START SESSION" button in details
