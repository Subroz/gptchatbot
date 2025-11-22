# 📋 Quick Reference Card

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Copy and edit .env
cp .env.example .env
nano .env  # Add your credentials

# 3. Run the bot
python3 telegram_ai_bot.py
```

---

## 🔑 Required Credentials

| Credential | Where to Get | Format |
|------------|--------------|--------|
| **API_ID** | https://my.telegram.org | 12345678 |
| **API_HASH** | https://my.telegram.org | abc123def456... |
| **BOT_TOKEN** | @BotFather on Telegram | 1234:ABC-DEF... |
| **OPENAI_API_KEY** | https://platform.openai.com | sk-proj-... |
| **OWNER_ID** | @userinfobot on Telegram | 123456789 |

---

## 📱 User Commands

```
/start     - Start bot & main menu
/ask       - Ask AI a question
/model     - Change AI model
/stats     - View usage statistics
/help      - Show help
```

**Natural Chat**: Just send messages directly (no command needed)

**Inline Mode**: `@yourbotusername your question` in any chat

---

## 👑 Owner Commands

```
/auth <user_id>      - Authorize user
/revoke <user_id>    - Revoke user access
/authgroup           - Authorize current group
/revokegroup         - Revoke group access
/ban <user_id>       - Ban user
/unban <user_id>     - Unban user
/broadcast <msg>     - Broadcast to all users
```

---

## 🤖 Available Models

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| **gpt-4o** | ⚡⚡⚡ | 💰💰💰 | Complex tasks |
| **gpt-4o-mini** | ⚡⚡⚡⚡ | 💰💰 | General use |
| **gpt-3.5-turbo** | ⚡⚡⚡⚡⚡ | 💰 | Quick queries |
| **o1-preview** | ⚡⚡ | 💰💰💰💰 | Deep reasoning |

---

## 🛠️ Management Scripts

```bash
# Using bot.sh
./bot.sh start        # Start bot
./bot.sh stop         # Stop bot
./bot.sh restart      # Restart bot
./bot.sh status       # Check status
./bot.sh logs         # View logs
./bot.sh logs -f      # Follow logs

# Manual management
python3 telegram_ai_bot.py                    # Run in foreground
nohup python3 telegram_ai_bot.py &           # Run in background
pkill -f telegram_ai_bot.py                  # Stop bot
tail -f bot.log                               # View logs
```

---

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

---

## 📊 File Structure

```
telegram-ai-bot/
├── telegram_ai_bot.py          ← Main bot code
├── requirements.txt             ← Dependencies
├── .env                        ← Your credentials
├── .env.example                ← Template
├── bot_data.json               ← Bot data (auto-created)
├── bot.log                     ← Logs (auto-created)
├── setup.sh                    ← Setup script
├── bot.sh                      ← Management script
├── README.md                   ← Main docs
├── CONFIGURATION.md            ← Setup guide
├── ADVANCED_USAGE.md           ← Advanced tips
└── QUICK_REFERENCE.md          ← This file
```

---

## 🔍 Troubleshooting

### Bot won't start
```bash
# Check configuration
cat .env

# Check logs
tail -100 bot.log

# Test dependencies
pip3 list | grep -E "pyrogram|openai"
```

### Bot not responding
1. Check if user is authorized
2. Verify bot is running: `./bot.sh status`
3. Check logs: `tail -f bot.log`
4. Restart: `./bot.sh restart`

### Inline mode not working
1. Enable via @BotFather: `/setinline`
2. Wait 2-3 minutes
3. Make sure user is authorized

### High costs
1. Check usage: `/stats`
2. Switch to cheaper models
3. Set OpenAI spending limits
4. Be more concise

---

## 💡 Usage Tips

### Efficient Questions
✅ **Good**: "Explain X in simple terms"
❌ **Bad**: "Can you maybe help me understand X if possible?"

### Model Selection
- Quick questions → `gpt-3.5-turbo`
- General use → `gpt-4o-mini`
- Complex tasks → `gpt-4o`
- Math/logic → `o1-preview`

### Cost Saving
- Be concise
- Use appropriate models
- Batch related questions
- Monitor with `/stats`

---

## 🔒 Security Checklist

- [ ] .env file is protected (chmod 600)
- [ ] .env in .gitignore
- [ ] API keys are private
- [ ] OpenAI spending limits set
- [ ] Only trusted users authorized
- [ ] Regular backups of bot_data.json

---

## 📞 Important Links

- **Telegram API**: https://my.telegram.org
- **BotFather**: https://t.me/BotFather
- **OpenAI Platform**: https://platform.openai.com
- **Get User ID**: https://t.me/userinfobot
- **Pyrogram Docs**: https://docs.pyrogram.org
- **OpenAI Docs**: https://platform.openai.com/docs

---

## ⚡ One-Liner Examples

```bash
# Complete setup
./setup.sh && python3 telegram_ai_bot.py

# Run in background with logs
nohup python3 telegram_ai_bot.py > bot.log 2>&1 & tail -f bot.log

# Check if running
ps aux | grep telegram_ai_bot.py

# Backup data
cp bot_data.json bot_data.backup.$(date +%Y%m%d).json

# View recent errors
grep -i error bot.log | tail -20
```

---

## 🎯 Common Scenarios

### First Time Setup
1. Run `./setup.sh`
2. Edit `.env` with credentials
3. Run `python3 telegram_ai_bot.py`
4. Test with `/start` in Telegram

### Authorize New User
1. Get their user ID (@userinfobot)
2. Send: `/auth <user_id>`
3. User can now use bot

### Authorize Group
1. Add bot to group
2. Send in group: `/authgroup`
3. Group can now use bot

### Change Default Model
1. Private chat with bot
2. Send: `/model`
3. Select preferred model

---

## 📈 Monitoring

```bash
# Check bot status
./bot.sh status

# Monitor logs in real-time
tail -f bot.log

# Check resource usage
ps aux | grep telegram_ai_bot.py

# View error count
grep -c ERROR bot.log
```

---

## 🆘 Emergency Commands

```bash
# Force stop bot
pkill -9 -f telegram_ai_bot.py

# Clear all data (CAUTION!)
rm bot_data.json bot.log

# Reset to defaults
cp .env.example .env
# Then edit .env with your credentials

# Full cleanup
pkill -f telegram_ai_bot.py && rm -f bot.pid *.log *.session
```

---

## 📝 Notes

- Bot logs rotate automatically
- Data is stored in `bot_data.json`
- Session files auto-created by Pyrogram
- First run may take longer (session creation)
- Restart bot after updating code

---

**Need more help?**
- Detailed setup → `CONFIGURATION.md`
- Advanced usage → `ADVANCED_USAGE.md`
- Full documentation → `README.md`

---

*Keep this card handy for quick reference! 📌*
