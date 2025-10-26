"""
Favicon Generator for Yogic Guide
Generates favicon from emoji using PIL
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def generate_favicon():
        """Generate favicon with yoga emoji"""
        
        # Create image with transparent background
        size = 512
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to use emoji font (system dependent)
        try:
            # Windows emoji font
            font = ImageFont.truetype("seguiemj.ttf", 400)
        except:
            try:
                # Mac emoji font
                font = ImageFont.truetype("Apple Color Emoji.ttc", 400)
            except:
                # Fallback to default
                font = ImageFont.load_default()
        
        # Draw emoji
        emoji = "🧘"
        
        # Get text size
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the emoji
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw emoji
        draw.text((x, y), emoji, font=font, embedded_color=True)
        
        # Save different sizes
        static_dir = 'static'
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        # Save 512x512 (original)
        img.save(os.path.join(static_dir, 'icon-512.png'))
        print("✅ Created: icon-512.png")
        
        # Save 192x192 (Android)
        img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
        img_192.save(os.path.join(static_dir, 'android-chrome-192x192.png'))
        print("✅ Created: android-chrome-192x192.png")
        
        # Save 180x180 (Apple)
        img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
        img_180.save(os.path.join(static_dir, 'apple-touch-icon.png'))
        print("✅ Created: apple-touch-icon.png")
        
        # Save 32x32 (Standard)
        img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
        img_32.save(os.path.join(static_dir, 'favicon-32x32.png'))
        print("✅ Created: favicon-32x32.png")
        
        # Save 16x16 (Small)
        img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
        img_16.save(os.path.join(static_dir, 'favicon-16x16.png'))
        print("✅ Created: favicon-16x16.png")
        
        # Convert to ICO (favicon.ico)
        img_32.save(os.path.join(static_dir, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32)])
        print("✅ Created: favicon.ico")
        
        print("\n🎉 All favicon files created successfully!")
        print(f"📁 Location: {os.path.abspath(static_dir)}")
        print("\n📋 Files created:")
        print("   - favicon.ico (16x16, 32x32)")
        print("   - favicon-16x16.png")
        print("   - favicon-32x32.png")
        print("   - apple-touch-icon.png (180x180)")
        print("   - android-chrome-192x192.png")
        print("   - icon-512.png")
        
    if __name__ == "__main__":
        print("🎨 Generating Yogic Guide Favicon...")
        print("=" * 50)
        generate_favicon()
        print("=" * 50)
        print("\n✅ Done! Restart your server to see the favicon.")
        
except ImportError:
    print("❌ PIL (Pillow) not installed!")
    print("\n📦 Install it with:")
    print("   pip install Pillow")
    print("\nOr download favicon from:")
    print("   https://favicon.io/emoji-favicons/person-in-lotus-position/")
