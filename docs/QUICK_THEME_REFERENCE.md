# ⚡ Quick Theme Reference - Professional Black & White

## 🎨 Color Codes

```css
Black: #000000
White: #FFFFFF
Gray-200: #e5e5e5
Gray-700: #404040
```

## 🔤 CSS Classes (Copy-Paste Ready)

### Buttons
```html
<button class="btn-professional">BUTTON TEXT</button>
<button class="btn-professional-outline">OUTLINE BUTTON</button>
```

### Cards
```html
<div class="card-professional">Content</div>
<div class="module-card-professional">Module Content</div>
<div class="stat-card-professional">Stats</div>
```

### Forms
```html
<label class="label-professional">LABEL</label>
<input class="input-professional" type="text">
<select class="select-professional">...</select>
```

### Typography
```html
<h1 class="text-professional-heading">HEADING</h1>
<p class="text-professional-body">Body text</p>
<span class="text-professional-muted">Muted text</span>
```

### Navigation
```html
<nav class="nav-professional">
    <a class="nav-link-professional">LINK</a>
</nav>
```

### Stats
```html
<p class="stat-label">LABEL</p>
<p class="stat-number">123</p>
```

### Effects
```html
<div class="hover-lift">Lifts on hover</div>
```

## 📱 Responsive Classes

```html
<!-- Mobile to Desktop -->
<div class="p-3 sm:p-6 md:p-8">Content</div>
<div class="text-sm sm:text-base md:text-lg">Text</div>
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-3">Grid</div>
```

## 🎯 Common Patterns

### Professional Button
```html
<a href="#" class="btn-professional px-8 py-4">
    START NOW
</a>
```

### Module Card
```html
<div class="module-card-professional">
    <div class="icon-container-professional mx-auto mb-6">
        🧘
    </div>
    <h2 class="text-professional-heading text-center">
        TITLE
    </h2>
    <p class="text-professional-body text-center">
        Description here
    </p>
    <button class="btn-professional w-full">
        ACTION →
    </button>
</div>
```

### Stat Display
```html
<div class="stat-card-professional hover-lift">
    <p class="stat-label">METRIC NAME</p>
    <p class="stat-number">1,234</p>
</div>
```

### Form Field
```html
<div>
    <label class="label-professional">FIELD NAME</label>
    <input class="input-professional" 
           type="text" 
           placeholder="Enter value">
</div>
```

### Admin Nav Link
```html
<a href="#" class="px-3 py-2 rounded 
              hover:bg-white hover:text-black 
              transition uppercase tracking-wide">
    LINK TEXT
</a>
```

## ✅ Quick Checklist

When adding new components:
- [ ] Use uppercase for emphasis
- [ ] Add letter-spacing (tracking-wide)
- [ ] Use black/white colors
- [ ] Add hover effects
- [ ] Make it responsive
- [ ] Test on mobile

## 🚀 Files to Include

In every HTML file:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/professional-theme.css') }}">
```

## 📊 Updated Pages

✅ Landing Page
✅ Dashboard
✅ Login
✅ Register
✅ Admin Base
✅ Admin Dashboard

---

**Quick Tip:** Copy-paste these classes directly into your HTML!
