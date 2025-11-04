# Module Cards - Hover Effects Guide

## 🎨 Visual Transformation

### Normal State → Hover State

```
NORMAL STATE:
┌─────────────────────────────────────┐
│                                     │
│         ┌─────────┐                 │
│         │         │                 │  Light gray gradient
│         │  🧘‍♀️    │                 │  Simple border
│         │         │                 │  Basic shadow
│         └─────────┘                 │
│                                     │
│    FULL BODY STRETCHING            │
│    Complete body flexibility...     │
│                                     │
│    ┌─────────────────────────┐     │
│    │ ⏱ Duration  [15-20 min] │     │
│    │ 📊 Level    [Beginner]  │     │
│    │ 🔥 Calories [~50 kcal]  │     │
│    └─────────────────────────┘     │
│                                     │
│    ┌─────────────────────────┐     │
│    │    VIEW DETAILS ↓       │     │
│    └─────────────────────────┘     │
│                                     │
└─────────────────────────────────────┘


HOVER STATE:
╔═════════════════════════════════════╗ ← Black accent bar slides in
║                                     ║
║         ┌─────────┐                 ║
║         │  ╱╲     │                 ║  Black gradient
║         │ ╱🧘‍♀️╲   │ ← Rotates 5°    ║  Glowing border
║         │╱    ╲  │    Scales 1.15  ║  Deep shadows
║         └─────────┘    Pulses      ║  Lifts up 12px
║                                     ║  Scales 1.02
║    FULL BODY STRETCHING            ║
║    Complete body flexibility...     ║
║                                     ║
║    ┌─────────────────────────┐     ║
║    │ ⏱ Duration  [15-20 min] │     ║  Enhanced badges
║    │ 📊 Level    [Beginner]  │     ║  Colored backgrounds
║    │ 🔥 Calories [~50 kcal]  │     ║
║    └─────────────────────────┘     ║
║                                     ║
║    ┌─────────────────────────┐     ║
║    │ ✨ VIEW DETAILS ↓ ✨    │     ║  Shimmer effect
║    └─────────────────────────┘     ║  Lifts + scales
║                                     ║
╚═════════════════════════════════════╝
        ↑ Entire card elevated
```

---

## 🎬 Animation Timeline

### When Mouse Enters Card:

```
Time: 0ms
├─ Top accent bar starts sliding in (left to right)
├─ Card border color begins changing to black
└─ Shadow starts deepening

Time: 100ms
├─ Icon background changes to black gradient
├─ Icon border glow appears
└─ Icon starts rotating and scaling

Time: 200ms
├─ Card lifts up (translateY: -12px)
├─ Card scales slightly (1.02)
└─ Radial overlay fades in

Time: 300ms
├─ Icon pulse animation begins
├─ Button shimmer starts
└─ Info badges enhance

Time: 400ms
├─ All animations complete
└─ Hover state fully active

Time: 600ms
└─ Icon pulse animation completes
```

---

## 🎯 Individual Element Effects

### 1. Card Container
```
Transform Sequence:
┌─────────┐
│ Normal  │  →  Hover starts
└─────────┘
     ↓
┌─────────┐
│ Lifting │  →  translateY(-12px)
└─────────┘
     ↓
┌─────────┐
│ Scaling │  →  scale(1.02)
└─────────┘
     ↓
┌─────────┐
│ Final   │  →  Elevated + Scaled
└─────────┘
```

### 2. Top Accent Bar
```
Animation:
[          ]  →  0% (hidden, scaleX: 0)
[█         ]  →  25%
[████      ]  →  50%
[████████  ]  →  75%
[██████████]  →  100% (full width, scaleX: 1)
```

### 3. Icon Container
```
Rotation + Scale:
    🧘‍♀️     →  Normal (scale: 1, rotate: 0deg)
     ↓
   ╱🧘‍♀️╲    →  Hover (scale: 1.15, rotate: 5deg)
     ↓
  ╱ 🧘‍♀️ ╲   →  Pulse peak (scale: 1.25, rotate: -5deg)
     ↓
   ╱🧘‍♀️╲    →  Pulse end (scale: 1.15, rotate: 5deg)
```

### 4. Button Shimmer
```
Shimmer Effect:
[VIEW DETAILS ↓]  →  Normal
[✨VIEW DETAILS ↓]  →  Shimmer starts (left)
[VIEW✨DETAILS ↓]  →  Shimmer middle
[VIEW DETAILS✨↓]  →  Shimmer right
[VIEW DETAILS ↓]  →  Shimmer exits
```

---

## 🎨 Color Transitions

### Card Border:
```
#e5e5e5 (gray-200)  →  #000000 (black)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Light gray              Pure black
```

### Icon Background:
```
linear-gradient(135deg, #f5f5f5, #e5e5e5)
                ↓
linear-gradient(135deg, #000000, #262626)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Light gradient          Black gradient
```

### Card Background:
```
linear-gradient(145deg, #ffffff, #fafafa)
                ↓
linear-gradient(145deg, #ffffff, #f5f5f5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
White → Off-white       White → Light gray
```

---

## 📏 Shadow Depth Progression

### Normal State:
```
Layer 1: 0 4px 6px -1px rgba(0,0,0,0.05)  ← Subtle
Layer 2: 0 2px 4px -1px rgba(0,0,0,0.03)  ← Very subtle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total depth: ~10px, very soft
```

### Hover State:
```
Layer 1: 0 20px 25px -5px rgba(0,0,0,0.12)  ← Deep
Layer 2: 0 10px 10px -5px rgba(0,0,0,0.08)  ← Medium
Layer 3: 0 0 0 1px rgba(0,0,0,0.05)         ← Border glow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total depth: ~30px, strong presence
```

---

## 🎯 Badge Styling

### Duration Badge:
```
Normal:
┌─────────────┐
│ 15-20 min   │  White bg, gray border
└─────────────┘

Hover:
┌─────────────┐
│ 15-20 min   │  Slightly enhanced
└─────────────┘
```

### Level Badge (Color-coded):
```
Beginner:
┌─────────────┐
│ Beginner    │  Indigo bg (#EEF2FF)
└─────────────┘  Indigo text (#4F46E5)

All Levels:
┌─────────────┐
│ All Levels  │  Blue bg (#DBEAFE)
└─────────────┘  Blue text (#2563EB)

Intermediate:
┌─────────────┐
│Intermediate │  Orange bg (#FFF7ED)
└─────────────┘  Orange text (#EA580C)
```

---

## 🎪 Complete Hover Experience

### User Interaction Flow:

1. **Mouse approaches card**
   - User sees normal state
   - Card is at rest position

2. **Mouse enters card boundary**
   - Top bar starts sliding in
   - Card begins lifting
   - Icon starts transforming

3. **Mouse hovers over card**
   - All animations active
   - Card fully elevated
   - Icon pulsing
   - Button shimmering

4. **Mouse hovers over button**
   - Button lifts additionally
   - Shimmer effect active
   - Shadow deepens more

5. **Mouse clicks button**
   - Button scales down (0.98)
   - Quick feedback
   - Details expand below

6. **Mouse leaves card**
   - All effects reverse
   - Smooth return to normal
   - Card settles back

---

## 💫 Special Effects

### 1. Radial Gradient Overlay
```
Position: Top-right corner
Size: 200% × 200%
Effect: Subtle light wash
Opacity: 0 → 1 on hover
```

### 2. Border Glow (Icon)
```
Technique: CSS mask with gradient
Effect: Animated border that glows
Colors: Black gradient
Opacity: 0 → 1 on hover
```

### 3. Shimmer (Button)
```
Technique: Pseudo-element animation
Effect: Light sweep across button
Speed: 0.5s
Direction: Left to right
```

---

## 🎨 Three Module Variations

### Full Body Stretching (Indigo Theme)
```
╔═════════════════════════════════════╗
║         🧘‍♀️                         ║
║    FULL BODY STRETCHING            ║
║    [Beginner] ← Indigo badge       ║
╚═════════════════════════════════════╝
```

### Breathing Exercises (Blue Theme)
```
╔═════════════════════════════════════╗
║         🌬️                          ║
║    BREATHING EXERCISES             ║
║    [All Levels] ← Blue badge       ║
╚═════════════════════════════════════╝
```

### Surya Namaskar (Orange Theme)
```
╔═════════════════════════════════════╗
║         ☀️                          ║
║    SURYA NAMASKAR                  ║
║    [Intermediate] ← Orange badge   ║
╚═════════════════════════════════════╝
```

---

## 🚀 Performance Notes

### GPU Acceleration:
- All transforms use `translate3d` or `scale`
- Opacity transitions are GPU-accelerated
- No layout reflows during animations

### Smooth Animations:
- Cubic-bezier easing: `cubic-bezier(0.4, 0, 0.2, 1)`
- 60fps target
- Hardware-accelerated properties

### Optimizations:
- `will-change` hints for transforms
- Composite layers for animations
- Minimal repaints

---

## ✨ Final Result

The module cards now provide:
- **Premium feel** with authentic depth
- **Engaging interactions** with smooth animations
- **Professional appearance** with clean design
- **Clear hierarchy** with enhanced badges
- **Delightful experience** with multiple effects

Perfect for a modern wellness application! 🧘‍♀️✨
