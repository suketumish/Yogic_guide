#!/usr/bin/env python3
"""
Test script to verify app.py works correctly
"""

import sys
import ast

def test_app_syntax():
    """Test if app.py has valid syntax"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse the AST to check syntax
        ast.parse(source_code)
        print("✅ app.py syntax is valid!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py:")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'Unknown'}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def test_app_imports():
    """Test if app.py imports work"""
    try:
        # Try to import the app module
        import app
        print("✅ app.py imports successfully!")
        print(f"✅ Flask app created: {type(app.app)}")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧘 Testing Zen_Align App")
    print("=" * 30)
    
    # Test syntax
    if not test_app_syntax():
        return False
    
    # Test imports
    if not test_app_imports():
        return False
    
    print("\n🎉 All tests passed! The app should work correctly.")
    print("\n💡 To start the app, run: python app.py")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)