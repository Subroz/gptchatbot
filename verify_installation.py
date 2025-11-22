#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all requirements are met before running the bot
"""

import sys
import os

def print_header(text):
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def print_status(status, message):
    symbols = {"pass": "✅", "fail": "❌", "warn": "⚠️", "info": "ℹ️"}
    print(f"{symbols.get(status, '•')} {message}")

def check_python_version():
    print_header("Checking Python Version")
    version = sys.version_info
    print_status("info", f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_status("pass", "Python version is compatible")
        return True
    else:
        print_status("fail", "Python 3.8+ required")
        return False

def check_dependencies():
    print_header("Checking Dependencies")
    required = ["pyrogram", "openai", "dotenv"]
    all_installed = True
    
    for package in required:
        module_name = "python-dotenv" if package == "dotenv" else package
        try:
            if package == "dotenv":
                import dotenv
            elif package == "pyrogram":
                import pyrogram
            elif package == "openai":
                import openai
            print_status("pass", f"{module_name} is installed")
        except ImportError:
            print_status("fail", f"{module_name} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Install missing dependencies with:")
        print("   pip3 install -r requirements.txt")
    
    return all_installed

def check_env_file():
    print_header("Checking Configuration")
    
    if not os.path.exists('.env'):
        print_status("fail", ".env file not found")
        print("\n💡 Create .env file:")
        print("   cp .env.example .env")
        print("   nano .env  # Edit with your credentials")
        return False
    
    print_status("pass", ".env file exists")
    
    # Check for placeholder values
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'OPENAI_API_KEY', 'OWNER_ID']
        placeholders = ['your_api_id_here', 'your_api_hash_here', 'your_bot_token_here', 
                       'your_openai_api_key_here', 'your_telegram_user_id_here']
        
        all_configured = True
        for var in required_vars:
            value = os.getenv(var, '')
            if not value or any(ph in value for ph in placeholders):
                print_status("fail", f"{var} not configured")
                all_configured = False
            else:
                masked = value[:8] + "..." if len(value) > 8 else "***"
                print_status("pass", f"{var} is set ({masked})")
        
        if not all_configured:
            print("\n💡 Edit .env and add your credentials")
            print("   Get credentials from:")
            print("   • API_ID & API_HASH: https://my.telegram.org")
            print("   • BOT_TOKEN: @BotFather on Telegram")
            print("   • OPENAI_API_KEY: https://platform.openai.com")
            print("   • OWNER_ID: @userinfobot on Telegram")
        
        return all_configured
        
    except Exception as e:
        print_status("warn", f"Could not validate .env: {e}")
        return True

def check_permissions():
    print_header("Checking File Permissions")
    
    if os.path.exists('telegram_ai_bot.py'):
        if os.access('telegram_ai_bot.py', os.R_OK):
            print_status("pass", "Bot script is readable")
        else:
            print_status("fail", "Cannot read bot script")
            return False
    else:
        print_status("fail", "telegram_ai_bot.py not found")
        return False
    
    # Check if we can create data file
    try:
        with open('test_write.tmp', 'w') as f:
            f.write('test')
        os.remove('test_write.tmp')
        print_status("pass", "Directory is writable")
    except:
        print_status("fail", "Cannot write to directory")
        return False
    
    return True

def main():
    print("""
╔══════════════════════════════════════════════════╗
║   Advanced Telegram AI Bot                      ║
║   Installation Verification                      ║
╚══════════════════════════════════════════════════╝
    """)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration", check_env_file),
        ("Permissions", check_permissions)
    ]
    
    results = []
    for name, check_func in checks:
        results.append(check_func())
    
    print_header("Summary")
    
    if all(results):
        print_status("pass", "All checks passed! ✨")
        print("\n🚀 You're ready to start the bot:")
        print("   python3 telegram_ai_bot.py")
        print("\nOr use the management script:")
        print("   ./bot.sh start")
        return 0
    else:
        print_status("fail", "Some checks failed")
        print("\n⚠️  Please fix the issues above before running the bot")
        print("\n📚 Documentation:")
        print("   • README.md - Full documentation")
        print("   • CONFIGURATION.md - Setup guide")
        print("   • QUICK_REFERENCE.md - Quick commands")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
