# Telegram AI Bot - Replit Setup

## Overview
Advanced Telegram bot powered by OpenAI's GPT models with inline mode support, user authentication, and usage tracking.

## Project Status
✅ **RUNNING** - Bot is live and connected to Telegram

## Recent Changes (Nov 22, 2025)
- Imported from GitHub repository
- Replaced `pyrogram` with `pyrotgfork` for better compatibility
- Configured environment secrets for API credentials
- Set up workflow to auto-run the bot

## Project Architecture

### Core Components
- **telegram_ai_bot.py** - Main bot application with all handlers
- **bot_data.json** - Persistent storage for users, groups, and stats (auto-created)
- **requirements.txt** - Python dependencies (pyrotgfork, tgcrypto, openai, python-dotenv)

### Key Features
1. **Multiple AI Models**: GPT-4o, GPT-4 Turbo, GPT-3.5, O1 models
2. **Inline Mode**: Use bot in any chat with @botusername
3. **Group Support**: Works in authorized groups
4. **User Management**: Owner can authorize/ban users
5. **Usage Tracking**: Monitors API usage per user/model

### Environment Secrets
Configured in Replit Secrets (DO NOT commit to git):
- `API_ID` - Telegram API ID from my.telegram.org
- `API_HASH` - Telegram API Hash
- `BOT_TOKEN` - Bot token from @BotFather
- `OPENAI_API_KEY` - OpenAI API key (sk-...)
- `OWNER_ID` - Telegram user ID for admin access

## Running the Bot
The bot runs automatically via the "Telegram AI Bot" workflow.
- **Status**: Check the Console tab
- **Logs**: Available in bot.log and Console output
- **Restart**: Click the Stop/Run button in the workflow

## Bot Commands

### User Commands
- `/start` - Initialize bot and show menu
- `/ask <question>` - Ask AI a question
- `/model` - Change preferred AI model
- `/stats` - View usage statistics
- `/help` - Show help information

### Owner Commands
- `/auth <user_id>` - Authorize user
- `/revoke <user_id>` - Revoke access
- `/authgroup` - Authorize group (use in group)
- `/revokegroup` - Revoke group access
- `/ban <user_id>` - Ban user
- `/unban <user_id>` - Unban user
- `/broadcast <message>` - Broadcast to all users

### Inline Mode
Type `@yourbotusername your question` in any chat

## File Structure
```
.
├── telegram_ai_bot.py       # Main bot code
├── requirements.txt          # Dependencies
├── bot_data.json            # Data storage (auto-created)
├── bot.log                  # Log file (auto-created)
├── ai_assistant_bot.session # Session file (auto-created)
├── .gitignore              # Ignore sensitive files
└── Documentation files (README, etc.)
```

## Development Notes

### Using pyrotgfork
This project uses `pyrotgfork` instead of the standard `pyrogram` library for better compatibility and active maintenance.

### Data Persistence
- User authorization, preferences, and stats are stored in `bot_data.json`
- Session data is stored in `.session` files (auto-generated)
- All sensitive files are excluded via .gitignore

### Monitoring
- Check Console tab for live bot activity
- Review `bot.log` for detailed logging
- Monitor OpenAI API usage at platform.openai.com

## Troubleshooting

### Bot Not Responding
1. Check Console tab - ensure bot is running
2. Verify environment secrets are set correctly
3. Check if user is authorized (owner is auto-authorized)
4. Review bot.log for errors

### OpenAI Errors
1. Verify OPENAI_API_KEY is valid
2. Check OpenAI account has credits
3. Confirm API key has proper permissions

### Connection Issues
1. Bot auto-reconnects on disconnect
2. Check Telegram API status
3. Verify API_ID and API_HASH are correct

## Security Notes
- All API keys stored as Replit Secrets
- Bot data file excluded from version control
- Session files are private to this Repl
- Only owner can manage user access by default
