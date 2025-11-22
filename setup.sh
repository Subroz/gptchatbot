#!/bin/bash

# Advanced Telegram AI Bot - Setup Script
# This script helps you set up the bot quickly

echo "🤖 Advanced Telegram AI Bot Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install requirements
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your credentials:"
    echo "   - API_ID (from https://my.telegram.org)"
    echo "   - API_HASH (from https://my.telegram.org)"
    echo "   - BOT_TOKEN (from @BotFather)"
    echo "   - OPENAI_API_KEY (from https://platform.openai.com)"
    echo "   - OWNER_ID (your Telegram user ID from @userinfobot)"
    echo ""
    echo "After editing .env, run: python3 telegram_ai_bot.py"
else
    echo "✅ .env file already exists"
    echo ""
    
    # Validate .env file
    echo "🔍 Validating configuration..."
    
    if grep -q "your_api_id_here" .env || grep -q "your_api_hash_here" .env || grep -q "your_bot_token_here" .env || grep -q "your_openai_api_key_here" .env || grep -q "your_telegram_user_id_here" .env; then
        echo "⚠️  WARNING: .env file contains default placeholder values!"
        echo "   Please update your credentials in .env file before running the bot."
    else
        echo "✅ Configuration looks good!"
        echo ""
        echo "🚀 You can now start the bot with:"
        echo "   python3 telegram_ai_bot.py"
        echo ""
        echo "Or run in background:"
        echo "   nohup python3 telegram_ai_bot.py > bot.log 2>&1 &"
    fi
fi

echo ""
echo "📚 For detailed instructions, check README.md"
echo "✨ Setup complete!"
