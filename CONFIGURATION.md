# 🔧 Configuration Guide

## Step-by-Step Setup Instructions

### 1. Get Telegram API Credentials

#### A. Visit Telegram's Developer Portal
1. Open your web browser
2. Go to: https://my.telegram.org
3. Log in using your phone number
4. Enter the verification code sent to your Telegram app

#### B. Create an Application
1. Click on "API development tools"
2. Fill in the application details:
   - **App title**: Choose any name (e.g., "My AI Bot")
   - **Short name**: Choose a short identifier (e.g., "aibot")
   - **Platform**: Choose "Other"
   - **Description**: Optional
3. Click "Create application"

#### C. Save Your Credentials
You'll receive:
- **api_id**: A number (e.g., 12345678)
- **api_hash**: A long string (e.g., 0123456789abcdef0123456789abcdef)

**Keep these safe and never share them!**

---

### 2. Create Your Telegram Bot

#### A. Contact BotFather
1. Open Telegram
2. Search for `@BotFather` (official bot with blue checkmark)
3. Start a chat with `/start`

#### B. Create New Bot
1. Send: `/newbot`
2. Choose a name for your bot (e.g., "My AI Assistant")
3. Choose a username ending in "bot" (e.g., "myai_assistant_bot")

#### C. Get Your Bot Token
BotFather will send you a token like:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789
```

**Copy this token and keep it safe!**

#### D. Enable Inline Mode
1. Send to BotFather: `/setinline`
2. Select your bot
3. Send a placeholder text (e.g., "Search...")

#### E. Enable Inline Feedback (Optional)
1. Send to BotFather: `/setinlinefeedback`
2. Select your bot
3. Choose "Enabled"

---

### 3. Get OpenAI API Key

#### A. Sign Up/Login
1. Go to: https://platform.openai.com
2. Sign up or log in with your account

#### B. Add Payment Method
1. Go to "Billing" in the menu
2. Add a payment method
3. Add credits (recommended: start with $5-10)

#### C. Create API Key
1. Go to "API keys" section
2. Click "Create new secret key"
3. Give it a name (e.g., "Telegram Bot")
4. Copy the key (starts with `sk-proj-` or `sk-`)

**⚠️ Important**: Save this key immediately! You won't be able to see it again.

#### D. Set Usage Limits (Recommended)
1. Go to "Limits" in settings
2. Set monthly spending limits
3. Enable email notifications for usage alerts

---

### 4. Get Your Telegram User ID

#### Method 1: Using @userinfobot
1. Open Telegram
2. Search for `@userinfobot`
3. Send any message
4. The bot will reply with your user ID (a number like 123456789)

#### Method 2: Using @raw_data_bot
1. Search for `@raw_data_bot`
2. Forward any of your messages to it
3. Look for "from" -> "id" in the response

---

### 5. Configure the .env File

Open the `.env` file and replace the placeholder values:

```env
# From my.telegram.org
API_ID=12345678
API_HASH=0123456789abcdef0123456789abcdef

# From @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789

# From platform.openai.com
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# From @userinfobot
OWNER_ID=123456789
```

---

### 6. Test Your Configuration

Run this command to verify everything is set up:

```bash
python3 -c "
from dotenv import load_dotenv
import os

load_dotenv()

print('Checking configuration...')
print('✓ API_ID:', 'Set' if os.getenv('API_ID') else '❌ Missing')
print('✓ API_HASH:', 'Set' if os.getenv('API_HASH') else '❌ Missing')
print('✓ BOT_TOKEN:', 'Set' if os.getenv('BOT_TOKEN') else '❌ Missing')
print('✓ OPENAI_API_KEY:', 'Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing')
print('✓ OWNER_ID:', 'Set' if os.getenv('OWNER_ID') else '❌ Missing')
"
```

---

## Common Issues and Solutions

### Issue: "Invalid API_ID or API_HASH"
**Solution**: 
- Double-check your credentials from my.telegram.org
- Make sure there are no extra spaces
- API_ID should be just numbers, no quotes needed in code

### Issue: "Invalid bot token"
**Solution**:
- Get a new token from @BotFather using `/token`
- Make sure you copied the entire token
- Check for any extra spaces or characters

### Issue: "OpenAI API Error: Invalid API Key"
**Solution**:
- Verify your API key is correct
- Check if the key is still active in OpenAI dashboard
- Make sure you've set up billing in OpenAI account

### Issue: "Bot doesn't respond"
**Solution**:
- Check if bot is running (look for logs)
- Verify user is authorized (owner needs to use `/auth <user_id>`)
- Check bot.log for error messages

### Issue: Inline mode not working
**Solution**:
- Enable inline mode via @BotFather (`/setinline`)
- Wait a few minutes for changes to propagate
- Make sure you're typing the correct bot username

---

## Security Checklist

- [ ] `.env` file is in `.gitignore` (never commit it!)
- [ ] API keys are kept private
- [ ] Bot token is not shared
- [ ] Set up OpenAI spending limits
- [ ] Only authorize trusted users
- [ ] Regularly review authorized users
- [ ] Monitor usage statistics
- [ ] Keep backup of `bot_data.json`

---

## Quick Reference

### File Structure
```
telegram-ai-bot/
├── telegram_ai_bot.py      # Main bot code
├── requirements.txt         # Python dependencies
├── .env                     # Your credentials (create this!)
├── .env.example            # Template file
├── setup.sh                # Setup script
├── README.md               # Documentation
├── CONFIGURATION.md        # This file
├── telegram-ai-bot.service # Systemd service
├── bot_data.json           # Bot data (auto-created)
└── bot.log                 # Logs (auto-created)
```

### Quick Commands
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run setup script
./setup.sh

# Start bot
python3 telegram_ai_bot.py

# Run in background
nohup python3 telegram_ai_bot.py > bot.log 2>&1 &

# Check logs
tail -f bot.log

# Stop background bot
pkill -f telegram_ai_bot.py
```

---

## Need Help?

1. Check the main README.md for troubleshooting
2. Review bot.log for error messages
3. Verify all credentials are correct
4. Make sure all required packages are installed
5. Check OpenAI account has credits
6. Ensure Telegram account is not restricted

---

**Ready to go? Start your bot with:**
```bash
python3 telegram_ai_bot.py
```

**Good luck! 🚀**
