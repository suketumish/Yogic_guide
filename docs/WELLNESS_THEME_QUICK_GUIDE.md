# 🌿 Wellness Theme - Quick Reference Guide

## 🎨 Color Palette (Copy-Paste Ready)

```css
/* Primary Colors */
--sage-green: #8B9D83;      /* Navigation, buttons, primary */
--olive-green: #6B7D63;     /* Text, links, accents */

/* Backgrounds */
--warm-ivory: #FDFBF7;      /* Main background */
--light-sand: #F5F1E8;      /* Secondary background */

/* Borders & Dividers */
--soft-sand: #E8DCC4;       /* Borders, cards */

/* Text & Accents */
--warm-taupe: #A89F91;      /* Subtle text, placeholders */
--terracotta: #C17B5C;      /* CTA buttons, highlights */
```

## 📝 Typography

```html
<!-- Google Fonts Import -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- CSS Classes -->
<style>
.yogic-heading {
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.1em;
}

.yogic-body {
    font-family: 'Poppins', sans-serif;
}
</style>
```

## 🎯 Common Components

### Navigation Bar
```html
<nav class="nav-wellness">
    <!-- Content -->
</nav>
```

### Button (Primary)
```html
<button class="yogic-body" style="background-color: #8B9D83; color: white;">
    Click Me
</button>
```

### Button (Secondary)
```html
<button class="yogic-body" style="background-color: white; color: #6B7D63;">
    Click Me
</button>
```

### Form Input
```html
<input class="yogic-body" style="border-color: #E8DCC4;" />
```

### Card
```html
<div style="background: white; border: 2px solid #E8DCC4;">
    <!-- Content -->
</div>
```

### Heading
```html
<h1 class="yogic-heading" style="color: #6B7D63;">
    Your Heading
</h1>
```

### Body Text
```html
<p class="yogic-body" style="color: #6B7D63;">
    Your text here
</p>
```

### Subtle Text
```html
<p class="yogic-body" style="color: #A89F91;">
    Subtle text
</p>
```

## 📁 CSS File

```html
<!-- Include in <head> -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/yogic-wellness-theme.css') }}">
```

## 🎨 Background Colors

```html
<!-- Main pages -->
<body style="background-color: #FDFBF7;">

<!-- Secondary sections -->
<section style="background-color: #F5F1E8;">

<!-- Cards -->
<div style="background-color: white;">
```

## 🔗 Links

```html
<!-- Primary link -->
<a class="yogic-body hover:opacity-80" style="color: #6B7D63;">
    Link Text
</a>

<!-- Subtle link -->
<a class="yogic-body hover:opacity-80" style="color: #A89F91;">
    Link Text
</a>
```

## 📱 Responsive Classes

```html
<!-- Text sizes -->
text-xs sm:text-sm md:text-base lg:text-lg

<!-- Padding -->
px-3 sm:px-4 md:px-6 lg:px-8
py-2 sm:py-3 md:py-4 lg:py-6

<!-- Font sizes for headings -->
text-2xl sm:text-3xl md:text-4xl lg:text-5xl
```

## 🎯 Page Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Page - Yogic Guide</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
    
    <!-- Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/animations.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/mobile-responsive.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/yogic-wellness-theme.css') }}">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        .yogic-heading {
            font-family: 'Playfair Display', serif;
            letter-spacing: 0.1em;
        }
        .yogic-body {
            font-family: 'Poppins', sans-serif;
        }
    </style>
</head>
<body style="background-color: #F5F1E8;" class="min-h-screen">
    <!-- Your content -->
</body>
</html>
```

## 🌟 Common Patterns

### Hero Section
```html
<section style="background: linear-gradient(135deg, #8B9D83 0%, #9BA17B 100%);" class="py-20">
    <h1 class="yogic-heading text-white">Your Heading</h1>
    <p class="yogic-body text-white opacity-90">Your text</p>
</section>
```

### Feature Card
```html
<div class="bg-white rounded-2xl p-8 shadow-lg" style="border: 2px solid #E8DCC4;">
    <div class="text-5xl mb-4">🧘</div>
    <h3 class="yogic-heading text-2xl mb-3" style="color: #6B7D63;">Feature Title</h3>
    <p class="yogic-body" style="color: #A89F91;">Description</p>
</div>
```

### Form Group
```html
<div>
    <label class="yogic-body block text-sm font-bold mb-2" style="color: #6B7D63;">
        Label
    </label>
    <input 
        class="yogic-body w-full px-4 py-3 border-2 rounded-lg focus:outline-none" 
        style="border-color: #E8DCC4;"
        placeholder="Enter value"
    />
</div>
```

## 🎨 Hover Effects

```css
/* Button hover */
.btn:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(139, 157, 131, 0.3);
}

/* Link hover */
.link:hover {
    opacity: 0.8;
}

/* Card hover */
.card:hover {
    transform: translateY(-5px);
    border-color: #8B9D83;
    box-shadow: 0 8px 24px rgba(139, 157, 131, 0.15);
}
```

## 📊 Spacing Guidelines

```
Small:   4px  (0.25rem)
Medium:  8px  (0.5rem)
Large:   16px (1rem)
XLarge:  24px (1.5rem)
XXLarge: 32px (2rem)
```

## 🎯 When to Use Each Color

**Sage Green (#8B9D83):**
- Navigation bars
- Primary buttons
- Section backgrounds
- Active states

**Olive Green (#6B7D63):**
- Headings
- Body text
- Links
- Icons

**Warm Ivory (#FDFBF7):**
- Main page background
- Card backgrounds

**Light Sand (#F5F1E8):**
- Secondary sections
- Alternate backgrounds

**Soft Sand (#E8DCC4):**
- Borders
- Dividers
- Card outlines

**Warm Taupe (#A89F91):**
- Subtle text
- Placeholders
- Disabled states

**Terracotta (#C17B5C):**
- Call-to-action buttons
- Important highlights
- Special features

## ✅ Quick Checklist

When creating a new page:
- [ ] Include yogic-wellness-theme.css
- [ ] Add Google Fonts (Playfair + Poppins)
- [ ] Set background to #F5F1E8 or #FDFBF7
- [ ] Use .yogic-heading for headings
- [ ] Use .yogic-body for text
- [ ] Use wellness colors
- [ ] Add favicon
- [ ] Test responsiveness
- [ ] Check for CSS errors

---

**Quick tip:** Copy this guide and keep it handy when building new pages! 🌿
