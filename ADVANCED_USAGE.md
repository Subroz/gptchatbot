# 🚀 Advanced Usage Guide

## Table of Contents
1. [Power User Tips](#power-user-tips)
2. [Inline Mode Mastery](#inline-mode-mastery)
3. [Group Chat Strategies](#group-chat-strategies)
4. [Model Selection Guide](#model-selection-guide)
5. [Cost Optimization](#cost-optimization)
6. [Administration Best Practices](#administration-best-practices)
7. [Advanced Scenarios](#advanced-scenarios)

---

## Power User Tips

### 1. Quick Context Switching
Switch models on the fly for different tasks:
```
Morning: gpt-4o-mini for quick emails and summaries
Afternoon: gpt-4o for complex problem-solving
Evening: gpt-3.5-turbo for casual conversation
```

### 2. Natural Conversation Flow
In private chats, skip the `/ask` command:
```
You: I'm learning Python
Bot: That's great! Python is...

You: Can you explain decorators?
Bot: Sure! Decorators in Python...
```

### 3. Efficient Question Formatting
**Good**: "Explain quantum entanglement in simple terms"
**Better**: "Explain quantum entanglement as if I'm 12 years old"
**Best**: "Explain quantum entanglement using everyday analogies, suitable for a beginner"

---

## Inline Mode Mastery

### Quick Facts
```
@yourbot capital of Japan
@yourbot 2+2*5
@yourbot translate "hello" to Spanish
```

### In Group Chats
Use inline mode without adding the bot:
```
In any group: @yourbot What is Docker?
→ Share AI answer instantly
```

### Pro Tips
1. **Shorter is Better**: Keep queries under 100 characters
2. **Be Specific**: "Python list comprehension example" > "Python lists"
3. **Multiple Attempts**: Try rephrasing if the answer isn't perfect

### Common Inline Use Cases
- **Quick translations**: `@yourbot translate "..." to French`
- **Math calculations**: `@yourbot solve x^2 + 5x + 6 = 0`
- **Code snippets**: `@yourbot Python function to reverse string`
- **Definitions**: `@yourbot define recursion`
- **Facts**: `@yourbot who invented the telephone`

---

## Group Chat Strategies

### Setup for Teams
1. Owner authorizes the group: `/authgroup`
2. Set group rules (optional)
3. Pin bot commands for easy reference

### Best Practices
**Do:**
- Use `/ask` prefix for clarity in busy groups
- Choose faster models (gpt-4o-mini, gpt-3.5-turbo)
- Set context in your question

**Don't:**
- Spam the bot with rapid-fire questions
- Use for private/sensitive information
- Expect long conversations (use private chat instead)

### Team Use Cases
```
Code Reviews:
/ask Review this Python code: [code snippet]

Documentation:
/ask Explain this API endpoint: [description]

Brainstorming:
/ask Give me 5 creative names for a project management app

Quick Research:
/ask What are the pros and cons of microservices?
```

---

## Model Selection Guide

### Model Characteristics

#### GPT-4o (Premium Choice)
- **Best for**: Complex reasoning, creative writing, detailed analysis
- **Speed**: Medium-Fast
- **Cost**: Highest
- **When to use**: 
  - Writing important documents
  - Solving complex problems
  - Code architecture decisions
  - Creative projects

#### GPT-4o Mini (Balanced)
- **Best for**: Everyday tasks, quick questions, general use
- **Speed**: Fast
- **Cost**: Low
- **When to use**:
  - Daily conversations
  - Quick facts
  - Simple coding tasks
  - General questions

#### GPT-3.5 Turbo (Economy)
- **Best for**: Simple queries, casual chat
- **Speed**: Very Fast
- **Cost**: Lowest
- **When to use**:
  - Testing/experimentation
  - Simple calculations
  - Basic information lookup
  - High-volume tasks

#### O1 Preview (Specialist)
- **Best for**: Complex reasoning, math, logic
- **Speed**: Slower
- **Cost**: Very High
- **When to use**:
  - Advanced mathematics
  - Complex logical problems
  - Strategic planning
  - Deep analysis

### Decision Flow
```
Simple question? → gpt-3.5-turbo or gpt-4o-mini
Complex task? → gpt-4o
Mathematical/logical? → o1-preview or o1-mini
Cost-sensitive? → gpt-4o-mini
Time-sensitive? → gpt-3.5-turbo
```

---

## Cost Optimization

### Understanding Costs
- Costs are per 1,000 tokens
- Input tokens (your question) + Output tokens (bot's answer)
- Roughly 750 words = 1,000 tokens

### Money-Saving Tips

#### 1. Use Appropriate Models
```
❌ Bad: Using gpt-4o for "What's 2+2?"
✅ Good: Using gpt-3.5-turbo for simple math
```

#### 2. Be Concise
```
❌ Bad: "I was wondering if you could possibly help me understand..."
✅ Good: "Explain [topic] briefly"
```

#### 3. Batch Questions
```
❌ Bad: Three separate questions
✅ Good: "Answer these three: 1) ... 2) ... 3) ..."
```

#### 4. Monitor Usage
- Check `/stats` regularly
- Set personal limits
- Switch to cheaper models when appropriate

### Estimated Costs (approximate)
```
gpt-3.5-turbo:  ~$0.001 per interaction
gpt-4o-mini:    ~$0.01 per interaction
gpt-4o:         ~$0.03 per interaction
o1-preview:     ~$0.15 per interaction
```

---

## Administration Best Practices

### User Management Strategy

#### Whitelist Approach (Recommended)
```
1. Start with owner only
2. Authorize trusted users manually: /auth <user_id>
3. Review user list monthly
4. Revoke inactive users: /revoke <user_id>
```

#### Group Management
```
1. Authorize groups explicitly: /authgroup
2. Monitor group usage
3. Set expectations (response times, appropriate use)
4. Revoke if misused: /revokegroup
```

### Monitoring

#### Daily Checks
- Review bot.log for errors
- Check unusual usage patterns
- Verify bot responsiveness

#### Weekly Checks
- Review usage statistics
- Check OpenAI billing
- Update authorized users list
- Backup bot_data.json

#### Monthly Checks
- Analyze cost trends
- Review model usage distribution
- Update bot if needed
- Clean up old logs

### Security

#### API Key Protection
```bash
# Never commit .env
echo ".env" >> .gitignore

# Restrict file permissions
chmod 600 .env

# Rotate keys periodically
# Update in OpenAI dashboard and .env
```

#### Bot Token Security
- Never share bot token
- Regenerate if compromised (@BotFather → `/token`)
- Use separate bots for testing/production

---

## Advanced Scenarios

### Scenario 1: Research Assistant

**Setup**: Set model to gpt-4o

**Usage**:
```
/ask Summarize the key points of [topic]
/ask What are the latest developments in [field]?
/ask Compare [concept A] and [concept B]
```

### Scenario 2: Code Helper

**Setup**: gpt-4o for architecture, gpt-4o-mini for simple tasks

**Usage**:
```
/ask Explain this error: [error message]
/ask Write a Python function to [task]
/ask Review this code for bugs: [code]
/ask Suggest improvements for [code]
```

### Scenario 3: Learning Companion

**Setup**: gpt-4o for explanations

**Usage**:
```
/ask Explain [concept] with examples
/ask What's the difference between [A] and [B]?
/ask Create a study guide for [topic]
/ask Quiz me on [subject]
```

### Scenario 4: Writing Assistant

**Setup**: gpt-4o for creative writing

**Usage**:
```
/ask Draft an email about [topic]
/ask Improve this paragraph: [text]
/ask Suggest alternatives for [phrase]
/ask Check grammar: [text]
```

### Scenario 5: Data Analysis Helper

**Setup**: gpt-4o or o1-preview

**Usage**:
```
/ask Analyze this data pattern: [data]
/ask What statistical test should I use for [scenario]?
/ask Explain this chart: [description]
```

---

## Workflow Examples

### Morning Routine
```
1. /model → Select gpt-4o-mini
2. /ask Summarize my calendar for today (if integrated)
3. Natural chat for quick questions
4. Use inline mode for team updates
```

### Development Session
```
1. /model → Select gpt-4o
2. Keep private chat open for questions
3. Use /ask for specific coding problems
4. Switch to gpt-3.5-turbo for simple syntax questions
```

### Research Mode
```
1. /model → Select gpt-4o
2. Start with broad questions
3. Drill down into specifics
4. Use /stats to monitor token usage
5. Switch to cheaper model for clarifications
```

---

## Troubleshooting Common Issues

### Bot is Slow
1. Check model (o1-preview is slower)
2. Simplify questions
3. Check OpenAI status
4. Try gpt-4o-mini for faster responses

### High Costs
1. Review /stats
2. Switch to cheaper models
3. Be more concise
4. Batch questions
5. Set OpenAI spending limits

### Inconsistent Responses
1. Be more specific in questions
2. Provide context
3. Try rephrasing
4. Switch to better model (gpt-4o)

### Authorization Issues
1. Verify user is authorized: `/auth <user_id>`
2. Check for bans in bot_data.json
3. For groups, use `/authgroup`
4. Restart bot if needed

---

## Pro Tips Summary

1. **Match model to task** - Don't use premium models for simple tasks
2. **Be specific** - Clear questions get better answers
3. **Use inline mode** - Perfect for quick, public questions
4. **Monitor costs** - Check /stats and OpenAI dashboard regularly
5. **Batch questions** - More efficient than asking one by one
6. **Natural conversation** - Skip commands in private chats
7. **Group management** - Authorize selectively, monitor actively
8. **Security first** - Protect API keys, review users regularly
9. **Learn patterns** - Note which models work best for your tasks
10. **Experiment** - Try different approaches to find what works

---

## Getting Help

Can't find what you need?
1. Check the main README.md
2. Review CONFIGURATION.md
3. Check bot.log for errors
4. Review OpenAI documentation
5. Check Telegram Bot API docs

---

**Happy chatting! 🎉**

*Remember: The bot is a tool to enhance your productivity, not replace your thinking!*
