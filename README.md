# 🤖 Advanced Telegram AI Bot

A high-end Telegram bot powered by OpenAI's GPT models with advanced features including inline mode, user/group authentication, model selection, and comprehensive usage tracking.

## ✨ Features

### Core Features
- 🤖 **Multiple AI Models**: Support for GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo, O1 Preview, and more
- 💬 **Natural Conversation**: Chat naturally with AI in private messages
- 🔍 **Inline Mode**: Use the bot in any chat with `@botusername query`
- 👥 **Group Support**: Works in authorized groups
- 🔐 **Authentication System**: User and group-level access control
- 📊 **Usage Statistics**: Track API usage per user and model
- 🎯 **Model Selection**: Each user can choose their preferred AI model
- 📢 **Broadcast System**: Owner can broadcast messages to all users

### Security Features
- Owner-only commands for user management
- User authorization/revocation system
- Group authorization system
- User ban/unban functionality
- Secure data storage

### User Experience
- Interactive inline keyboards
- Real-time typing indicators
- Clean, formatted responses
- Token usage tracking
- Model-specific statistics

## 📋 Prerequisites

1. **Telegram Account**
   - Active Telegram account
   - API credentials from https://my.telegram.org

2. **Bot Token**
   - Create a bot via [@BotFather](https://t.me/BotFather)
   - Enable inline mode in bot settings

3. **OpenAI API Key**
   - Sign up at https://platform.openai.com
   - Create an API key
   - Ensure you have credits/billing set up

## 🚀 Installation

### Step 1: Clone or Download
```bash
# If you have git
git clone <repository-url>
cd telegram-ai-bot

# Or download the files manually
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your credentials:
```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OWNER_ID=123456789
```

#### How to Get Credentials:

**API_ID and API_HASH:**
1. Visit https://my.telegram.org
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy your `api_id` and `api_hash`

**BOT_TOKEN:**
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided
4. Send `/setinline` to enable inline mode
5. Send `/setinlinefeedback` and choose "Enabled"

**OPENAI_API_KEY:**
1. Visit https://platform.openai.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new secret key
5. Copy the key (starts with `sk-`)

**OWNER_ID:**
1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send any message to get your user ID
3. Copy your ID number

### Step 4: Run the Bot
```bash
python telegram_ai_bot.py
```

The bot will start and log activities to both console and `bot.log` file.

## 📖 Usage Guide

### Basic Commands

#### For All Users:
- `/start` - Start the bot and see the main menu
- `/ask <question>` - Ask the AI a question
- `/model` - Change your preferred AI model
- `/stats` - View your usage statistics
- `/help` - Display help information

#### Owner-Only Commands:
- `/auth <user_id>` - Authorize a user to use the bot
- `/revoke <user_id>` - Revoke user's access
- `/authgroup` - Authorize the current group (use in group)
- `/revokegroup` - Revoke group's access (use in group)
- `/ban <user_id>` - Ban a user from using the bot
- `/unban <user_id>` - Unban a user
- `/broadcast <message>` - Send a message to all authorized users

### Using Inline Mode

Type `@yourbotusername your question` in any chat (including groups where the bot isn't added):

```
@yourbotusername What is quantum computing?
```

The bot will provide an instant AI response that you can send to the chat.

### Natural Conversation

In private chats, just send messages directly without commands for natural conversation:

```
You: Hello! How are you?
Bot: Hello! I'm doing great, thank you for asking! How can I help you today?
```

## 🎯 Available AI Models

| Model | Description | Best For |
|-------|-------------|----------|
| **gpt-4o** | Most capable model | Complex tasks, reasoning |
| **gpt-4o-mini** | Fast and efficient | Quick responses, general tasks |
| **gpt-4-turbo** | High performance | Advanced conversations |
| **gpt-4** | Original GPT-4 | High-quality responses |
| **gpt-3.5-turbo** | Fast and cost-effective | Simple queries |
| **o1-preview** | Advanced reasoning | Complex problem-solving |
| **o1-mini** | Fast reasoning | Quick logical tasks |

## 🔧 Configuration

### Data Storage

The bot stores data in `bot_data.json`:
- Authorized users list
- Authorized groups list
- User preferences (selected models)
- Usage statistics
- Banned users list

### Logging

Logs are saved to `bot.log` with the following information:
- Bot startup/shutdown
- API calls and responses
- Errors and exceptions
- User interactions

## 🛡️ Security Best Practices

1. **Keep Your Keys Safe**
   - Never commit `.env` file to version control
   - Don't share your API keys or bot token
   - Use environment variables in production

2. **User Management**
   - Start with a whitelist approach (authorize users manually)
   - Regularly review authorized users
   - Use the ban feature for abusive users

3. **API Usage**
   - Monitor usage statistics regularly
   - Set up OpenAI usage limits in your account
   - Consider implementing rate limiting for heavy usage

4. **Group Usage**
   - Only authorize trusted groups
   - Monitor group usage to prevent abuse
   - Revoke access from inactive groups

## 📊 Usage Statistics

The bot tracks:
- Total requests per user
- Total tokens consumed
- Usage per model
- Request counts by model

Access your stats with `/stats` command.

## 🔄 Updates and Maintenance

### Updating the Bot
```bash
# Stop the bot (Ctrl+C)
# Pull latest changes or update files
git pull

# Restart the bot
python telegram_ai_bot.py
```

### Backup Data
```bash
# Backup your data file regularly
cp bot_data.json bot_data.backup.json
```

## 🐛 Troubleshooting

### Bot Not Responding
- Check if the bot is running
- Verify your bot token is correct
- Check if the user is authorized
- Review logs in `bot.log`

### Inline Mode Not Working
- Make sure inline mode is enabled via @BotFather
- Check the bot username is correct
- Verify user is authorized

### OpenAI API Errors
- Check your API key is valid
- Verify you have sufficient credits
- Check OpenAI service status
- Review API usage limits

### Permission Errors
- Ensure user is authorized (`/auth <user_id>`)
- For groups, use `/authgroup` command
- Check if user is banned

## 💡 Tips and Tricks

1. **Model Selection**: Start with `gpt-4o-mini` for cost-effective responses, switch to `gpt-4o` for complex tasks

2. **Inline Mode**: Perfect for quick facts or translations in group chats

3. **Natural Conversation**: Works best in private chats for extended conversations

4. **Group Usage**: Great for team collaboration with AI assistance

5. **Statistics**: Monitor your usage to optimize costs

## 📝 Example Conversations

### Basic Q&A
```
User: /ask What is the capital of France?
Bot: The capital of France is Paris. It's known as the "City of Light" and is famous for...
━━━━━━━━━━━━━━━
🤖 Model: gpt-4o-mini
🎯 Tokens: 87
```

### Natural Conversation
```
You: I need help with a Python function
Bot: I'd be happy to help! What kind of function are you trying to create?

You: A function to calculate fibonacci numbers
Bot: Here's an efficient implementation using memoization...
```

### Inline Query
```
@yourbot What's the weather like in Tokyo?
[Bot provides current weather information inline]
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

- This bot uses OpenAI's API which has usage costs
- Monitor your API usage to avoid unexpected charges
- The bot owner is responsible for API usage and costs
- Follow Telegram's Bot API terms of service
- Respect OpenAI's usage policies

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `bot.log`
3. Consult OpenAI documentation: https://platform.openai.com/docs
4. Check Telegram Bot API docs: https://core.telegram.org/bots/api

## 🔗 Useful Links

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Pyrogram Documentation](https://docs.pyrogram.org)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Models](https://platform.openai.com/docs/models)

---

**Built with ❤️ using Pyrogram and OpenAI API**

*Happy chatting with AI! 🚀*
