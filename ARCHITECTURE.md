# 🏗️ Bot Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram User                           │
│  (Sends messages via Telegram App)                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   Telegram Bot API                          │
│  (Handles message routing and delivery)                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Pyrogram Client Library                        │
│  (Python wrapper for Telegram Bot API)                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│           telegram_ai_bot.py (Main Bot)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Message Handlers                                     │ │
│  │  • Command Handler (/start, /ask, /model, etc.)      │ │
│  │  • Inline Query Handler                              │ │
│  │  • Callback Query Handler                            │ │
│  │  • Natural Conversation Handler                      │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Authentication System                                │ │
│  │  • User Authorization                                 │ │
│  │  • Group Authorization                                │ │
│  │  • Owner Validation                                   │ │
│  │  • Ban Management                                     │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Data Management (BotData Class)                      │ │
│  │  • User preferences                                   │ │
│  │  • Usage statistics                                   │ │
│  │  • Authorization lists                                │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   OpenAI API Client                         │
│  (Handles AI model requests)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│               OpenAI API Servers                            │
│  (GPT-4o, GPT-4o Mini, GPT-3.5, O1 models)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Message Flow
```
User → Telegram → Pyrogram → Bot Handlers → Authentication Check
                                                    ↓
                                              Authorized?
                                              ↓         ↓
                                            YES        NO
                                             ↓          ↓
                                    Process Request   Deny Access
                                             ↓
                                    Call OpenAI API
                                             ↓
                                    Format Response
                                             ↓
                                    Log Statistics
                                             ↓
                                    Send to User
```

### 2. Inline Query Flow
```
User types @bot query → Telegram → Pyrogram → Inline Handler
                                                    ↓
                                              Auth Check
                                                    ↓
                                              Get Model
                                                    ↓
                                            Call OpenAI
                                                    ↓
                                          Create Result
                                                    ↓
                                          Return Result
                                                    ↓
                                      User selects result
                                                    ↓
                                        Message sent to chat
```

### 3. Owner Command Flow
```
Owner → /auth <user_id> → Bot → Verify Owner → Update Auth List
                                                       ↓
                                                  Save to JSON
                                                       ↓
                                                 Send Confirmation
```

---

## Component Breakdown

### Core Components

#### 1. **Client Initialization**
```python
app = Client(
    "ai_assistant_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
```
- Creates Pyrogram client
- Authenticates with Telegram
- Manages bot session

#### 2. **OpenAI Integration**
```python
openai_client = OpenAI(api_key=OPENAI_API_KEY)
```
- Handles API requests
- Manages model selection
- Processes responses

#### 3. **Data Storage (BotData Class)**
```python
class BotData:
    - load_data()      # Load from JSON
    - save_data()      # Save to JSON
    - is_user_authorized()
    - authorize_user()
    - get_user_model()
    - log_usage()
```

---

## Message Handlers

### Command Handlers
```python
@app.on_message(filters.command("start"))
@app.on_message(filters.command("ask"))
@app.on_message(filters.command("model"))
@app.on_message(filters.command("stats"))
@app.on_message(filters.command("help"))

# Owner only
@app.on_message(filters.command("auth") & filters.user(OWNER_ID))
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
```

### Inline Query Handler
```python
@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    # Process inline queries from any chat
```

### Callback Query Handler
```python
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    # Handle button presses (model selection, menu navigation)
```

### Natural Conversation Handler
```python
@app.on_message(filters.text & filters.private & ~filters.command(...))
async def natural_conversation_handler(client, message):
    # Handle direct messages without commands
```

---

## Authentication System

### Authorization Levels

```
┌──────────────────────────────────────┐
│         OWNER (OWNER_ID)             │
│  ✓ All commands                      │
│  ✓ User management                   │
│  ✓ Group authorization               │
│  ✓ Ban/Unban                         │
│  ✓ Broadcast                         │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│    AUTHORIZED USERS                  │
│  ✓ Basic commands                    │
│  ✓ Ask questions                     │
│  ✓ Change models                     │
│  ✓ View stats                        │
│  ✓ Natural conversation              │
│  ✓ Inline mode                       │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│    AUTHORIZED GROUPS                 │
│  ✓ /ask command                      │
│  ✓ Group queries                     │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│       UNAUTHORIZED                   │
│  ✗ Access denied                     │
└──────────────────────────────────────┘
```

---

## Data Storage Structure

### bot_data.json
```json
{
  "authorized_users": [123456, 789012, ...],
  "authorized_groups": [-100123456, ...],
  "banned_users": [555666, ...],
  "user_preferences": {
    "123456": {
      "model": "gpt-4o-mini"
    }
  },
  "usage_stats": {
    "123456": {
      "total_requests": 150,
      "total_tokens": 45000,
      "by_model": {
        "gpt-4o-mini": {
          "requests": 100,
          "tokens": 30000
        },
        "gpt-4o": {
          "requests": 50,
          "tokens": 15000
        }
      }
    }
  }
}
```

---

## Model Selection System

### Available Models Registry
```python
AVAILABLE_MODELS = {
    'gpt-4o': '🚀 GPT-4o (Most Capable)',
    'gpt-4o-mini': '⚡ GPT-4o Mini (Fast & Efficient)',
    'gpt-4-turbo': '🎯 GPT-4 Turbo',
    'gpt-4': '🧠 GPT-4',
    'gpt-3.5-turbo': '💨 GPT-3.5 Turbo',
    'o1-preview': '🔬 O1 Preview (Reasoning)',
    'o1-mini': '🎓 O1 Mini (Fast Reasoning)',
}
```

### Model Selection Flow
```
User clicks /model
      ↓
Display model keyboard
      ↓
User selects model
      ↓
Update user preference
      ↓
Save to bot_data.json
      ↓
Confirm to user
```

---

## API Integration

### OpenAI API Call Structure
```python
response = openai_client.chat.completions.create(
    model=user_selected_model,
    messages=[
        {"role": "system", "content": "system_prompt"},
        {"role": "user", "content": "user_question"}
    ],
    max_tokens=2000,
    temperature=0.7
)
```

### Response Processing
```
API Response → Extract content → Count tokens → Log usage
                                                     ↓
                                               Format message
                                                     ↓
                                              Send to user
```

---

## Error Handling

### Error Flow
```
Try:
    Execute operation
Except Exception:
    Log error → Format error message → Notify user
                                            ↓
                                    Log to bot.log
```

### Error Types Handled
- Network errors (Telegram/OpenAI)
- Authentication failures
- API rate limits
- Invalid commands
- Data storage errors
- Permission errors

---

## Logging System

### Log Levels
```
INFO  → General operations (startup, commands)
WARN  → Warnings (rate limits, retries)
ERROR → Errors (API failures, exceptions)
```

### Log Destinations
```
Console (stdout) → Real-time monitoring
bot.log file     → Persistent storage
```

---

## Session Management

### Pyrogram Session
```
ai_assistant_bot.session
    ↓
Stores authentication state
    ↓
Persists across restarts
    ↓
Auto-regenerates if deleted
```

---

## Performance Considerations

### Async Operations
```python
async def call_openai_api(...)  # Non-blocking API calls
async def message_handler(...)   # Concurrent message handling
```

### Typing Indicators
```python
await client.send_chat_action(chat_id, ChatAction.TYPING)
```
Shows user bot is processing

---

## Security Layers

```
┌─────────────────────────────────────┐
│  Layer 1: Telegram Authentication  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 2: Bot User Authorization   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 3: Owner Command Filtering  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 4: Ban List Check           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 5: Rate Limiting (planned)  │
└─────────────────────────────────────┘
```

---

## Scalability Features

### Concurrent Handling
- Async/await for non-blocking operations
- Multiple users handled simultaneously
- Queue management by Telegram

### Data Management
- JSON for simple persistence
- Easily upgradable to database
- Efficient in-memory operations

### Resource Usage
- Minimal memory footprint
- Efficient token management
- Optimized API calls

---

## Extension Points

### Easy to Add:
1. **New Models**: Add to `AVAILABLE_MODELS` dict
2. **New Commands**: Add handler with decorator
3. **New Features**: Implement as separate functions
4. **Database**: Replace `BotData` class
5. **Rate Limiting**: Add middleware
6. **Admin Panel**: Extend owner commands

---

## Deployment Architecture

### Option 1: Direct Python
```
OS → Python Interpreter → Bot Process
```

### Option 2: Docker
```
Docker Engine → Container → Python → Bot
```

### Option 3: Systemd Service
```
Systemd → Service Manager → Python → Bot
              ↓
         Auto-restart on failure
```

---

## Monitoring Points

### Key Metrics to Monitor
- Request count per user
- Token usage per model
- API response times
- Error rates
- Active users count
- Group activity

### Log Analysis
```bash
# Error count
grep ERROR bot.log | wc -l

# Most active users
grep "User ID:" bot.log | sort | uniq -c | sort -rn

# API calls today
grep "$(date +%Y-%m-%d)" bot.log | grep "OpenAI API" | wc -l
```

---

## Future Enhancements

### Possible Additions
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Redis caching
- [ ] Rate limiting per user
- [ ] Conversation history storage
- [ ] Web dashboard for analytics
- [ ] Webhook mode (instead of polling)
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Image generation integration
- [ ] Payment system integration

---

This architecture provides a solid foundation for a production-ready Telegram AI bot with room for growth and customization! 🚀
