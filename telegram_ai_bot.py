#!/usr/bin/env python3
"""
Advanced Telegram AI Bot with OpenAI Integration
Features: Inline Mode, User Auth, Group Auth, Model Selection, Owner Controls
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message, InlineQuery, InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OWNER_ID = int(os.getenv('OWNER_ID', 0))

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Data storage
DATA_FILE = 'bot_data.json'

class BotData:
    """Manages bot data storage"""
    
    def __init__(self):
        self.data = self.load_data()
        
    def load_data(self) -> dict:
        """Load data from file"""
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'authorized_users': [],
                'authorized_groups': [],
                'user_preferences': {},
                'usage_stats': {},
                'banned_users': []
            }
    
    def save_data(self):
        """Save data to file"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def is_user_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        return (
            user_id == OWNER_ID or
            user_id in self.data['authorized_users'] or
            user_id not in self.data['banned_users']
        )
    
    def is_group_authorized(self, chat_id: int) -> bool:
        """Check if group is authorized"""
        return chat_id in self.data['authorized_groups']
    
    def authorize_user(self, user_id: int):
        """Authorize a user"""
        if user_id not in self.data['authorized_users']:
            self.data['authorized_users'].append(user_id)
            self.save_data()
    
    def authorize_group(self, chat_id: int):
        """Authorize a group"""
        if chat_id not in self.data['authorized_groups']:
            self.data['authorized_groups'].append(chat_id)
            self.save_data()
    
    def revoke_user(self, user_id: int):
        """Revoke user authorization"""
        if user_id in self.data['authorized_users']:
            self.data['authorized_users'].remove(user_id)
            self.save_data()
    
    def revoke_group(self, chat_id: int):
        """Revoke group authorization"""
        if chat_id in self.data['authorized_groups']:
            self.data['authorized_groups'].remove(chat_id)
            self.save_data()
    
    def ban_user(self, user_id: int):
        """Ban a user"""
        if user_id not in self.data['banned_users']:
            self.data['banned_users'].append(user_id)
            self.save_data()
    
    def unban_user(self, user_id: int):
        """Unban a user"""
        if user_id in self.data['banned_users']:
            self.data['banned_users'].remove(user_id)
            self.save_data()
    
    def get_user_model(self, user_id: int) -> str:
        """Get user's preferred model"""
        return self.data['user_preferences'].get(str(user_id), {}).get('model', 'gpt-4o-mini')
    
    def set_user_model(self, user_id: int, model: str):
        """Set user's preferred model"""
        user_id_str = str(user_id)
        if user_id_str not in self.data['user_preferences']:
            self.data['user_preferences'][user_id_str] = {}
        self.data['user_preferences'][user_id_str]['model'] = model
        self.save_data()
    
    def log_usage(self, user_id: int, model: str, tokens: int):
        """Log API usage"""
        user_id_str = str(user_id)
        if user_id_str not in self.data['usage_stats']:
            self.data['usage_stats'][user_id_str] = {
                'total_requests': 0,
                'total_tokens': 0,
                'by_model': {}
            }
        
        stats = self.data['usage_stats'][user_id_str]
        stats['total_requests'] += 1
        stats['total_tokens'] += tokens
        
        if model not in stats['by_model']:
            stats['by_model'][model] = {'requests': 0, 'tokens': 0}
        
        stats['by_model'][model]['requests'] += 1
        stats['by_model'][model]['tokens'] += tokens
        self.save_data()

# Initialize bot data
bot_data = BotData()

# Available AI models
AVAILABLE_MODELS = {
    'gpt-4o': '🚀 GPT-4o (Most Capable)',
    'gpt-4o-mini': '⚡ GPT-4o Mini (Fast & Efficient)',
    'gpt-4-turbo': '🎯 GPT-4 Turbo',
    'gpt-4': '🧠 GPT-4',
    'gpt-3.5-turbo': '💨 GPT-3.5 Turbo',
    'o1-preview': '🔬 O1 Preview (Reasoning)',
    'o1-mini': '🎓 O1 Mini (Fast Reasoning)',
}

# Initialize Pyrogram client
app = Client(
    "ai_assistant_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def is_owner(user_id: int) -> bool:
    """Check if user is the owner"""
    return user_id == OWNER_ID

def create_model_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for model selection"""
    buttons = []
    for model_id, model_name in AVAILABLE_MODELS.items():
        buttons.append([InlineKeyboardButton(
            model_name,
            callback_data=f"model_{model_id}"
        )])
    return InlineKeyboardMarkup(buttons)

def create_main_menu() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    buttons = [
        [InlineKeyboardButton("🤖 Change Model", callback_data="change_model")],
        [InlineKeyboardButton("📊 Usage Stats", callback_data="stats")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    return InlineKeyboardMarkup(buttons)

async def call_openai_api(messages: list, model: str, max_tokens: int = 2000) -> tuple:
    """Call OpenAI API and return response with token count"""
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        return content, tokens
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    
    if not bot_data.is_user_authorized(user.id):
        await message.reply_text(
            "❌ **Access Denied**\n\n"
            "You are not authorized to use this bot.\n"
            "Please contact the bot owner for access."
        )
        return
    
    welcome_text = f"""
🤖 **Welcome to Advanced AI Assistant Bot!**

Hello {user.mention}! I'm powered by OpenAI's latest models.

**Features:**
• 💬 Chat with AI in private or groups
• 🔍 Inline mode for quick queries
• 🤖 Multiple AI models to choose from
• 📊 Track your usage statistics

**Quick Start:**
• Use /ask <question> to ask me anything
• Use /model to change AI model
• Type @{(await client.get_me()).username} <query> in any chat for inline mode

Ready to assist you! 🚀
    """
    
    await message.reply_text(
        welcome_text,
        reply_markup=create_main_menu()
    )

@app.on_message(filters.command("model"))
async def model_command(client: Client, message: Message):
    """Handle /model command"""
    if not bot_data.is_user_authorized(message.from_user.id):
        await message.reply_text("❌ Unauthorized access.")
        return
    
    current_model = bot_data.get_user_model(message.from_user.id)
    
    text = f"**🤖 Select Your AI Model**\n\n"
    text += f"Current: `{current_model}`\n\n"
    text += "Choose a model below:"
    
    await message.reply_text(
        text,
        reply_markup=create_model_keyboard()
    )

@app.on_message(filters.command("ask"))
async def ask_command(client: Client, message: Message):
    """Handle /ask command"""
    user_id = message.from_user.id
    
    # Check authorization for private chats
    if message.chat.type == enums.ChatType.PRIVATE:
        if not bot_data.is_user_authorized(user_id):
            await message.reply_text("❌ You are not authorized to use this bot.")
            return
    else:
        # Check group authorization
        if not bot_data.is_group_authorized(message.chat.id):
            await message.reply_text("❌ This group is not authorized to use this bot.")
            return
    
    # Extract question
    question = message.text.split(maxsplit=1)
    if len(question) < 2:
        await message.reply_text("❓ Please provide a question.\n\nUsage: `/ask your question here`")
        return
    
    question_text = question[1]
    
    # Get user's model preference
    model = bot_data.get_user_model(user_id)
    
    # Send typing action
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    
    # Show processing message
    processing_msg = await message.reply_text("🤔 Thinking...")
    
    try:
        # Call OpenAI API
        messages = [
            {"role": "system", "content": "You are a helpful, intelligent AI assistant. Provide clear, accurate, and concise responses."},
            {"role": "user", "content": question_text}
        ]
        
        response, tokens = await call_openai_api(messages, model)
        
        # Log usage
        bot_data.log_usage(user_id, model, tokens)
        
        # Format response
        response_text = f"{response}\n\n"
        response_text += f"━━━━━━━━━━━━━━━\n"
        response_text += f"🤖 Model: `{model}`\n"
        response_text += f"🎯 Tokens: `{tokens}`"
        
        await processing_msg.edit_text(response_text)
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        await processing_msg.edit_text(
            f"❌ **Error occurred:**\n`{str(e)}`\n\n"
            "Please try again later or contact support."
        )

@app.on_message(filters.command("stats"))
async def stats_command(client: Client, message: Message):
    """Handle /stats command"""
    user_id = message.from_user.id
    
    if not bot_data.is_user_authorized(user_id):
        await message.reply_text("❌ Unauthorized access.")
        return
    
    stats = bot_data.data['usage_stats'].get(str(user_id))
    
    if not stats:
        await message.reply_text("📊 No usage statistics available yet.")
        return
    
    text = "📊 **Your Usage Statistics**\n\n"
    text += f"🔢 Total Requests: `{stats['total_requests']}`\n"
    text += f"🎯 Total Tokens: `{stats['total_tokens']:,}`\n\n"
    text += "**By Model:**\n"
    
    for model, data in stats['by_model'].items():
        text += f"• `{model}`: {data['requests']} requests, {data['tokens']:,} tokens\n"
    
    await message.reply_text(text)

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
📚 **Bot Commands & Features**

**Basic Commands:**
• `/start` - Start the bot and see main menu
• `/ask <question>` - Ask AI a question
• `/model` - Change AI model
• `/stats` - View your usage statistics
• `/help` - Show this help message

**Inline Mode:**
Type `@botusername your question` in any chat to get instant AI responses!

**Owner Commands:**
• `/auth <user_id>` - Authorize user
• `/revoke <user_id>` - Revoke user access
• `/authgroup` - Authorize current group
• `/revokegroup` - Revoke group access
• `/ban <user_id>` - Ban user
• `/unban <user_id>` - Unban user
• `/broadcast <message>` - Broadcast to all users

**Available Models:**
    """
    
    for model_id, model_name in AVAILABLE_MODELS.items():
        help_text += f"• {model_name}\n"
    
    help_text += "\n🔥 Powered by OpenAI's cutting-edge AI technology!"
    
    await message.reply_text(help_text)

# Owner-only commands
@app.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def auth_command(client: Client, message: Message):
    """Authorize a user"""
    try:
        user_id = int(message.text.split()[1])
        bot_data.authorize_user(user_id)
        await message.reply_text(f"✅ User `{user_id}` has been authorized.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: `/auth <user_id>`")

@app.on_message(filters.command("revoke") & filters.user(OWNER_ID))
async def revoke_command(client: Client, message: Message):
    """Revoke user authorization"""
    try:
        user_id = int(message.text.split()[1])
        bot_data.revoke_user(user_id)
        await message.reply_text(f"✅ User `{user_id}` authorization has been revoked.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: `/revoke <user_id>`")

@app.on_message(filters.command("authgroup") & filters.user(OWNER_ID))
async def authgroup_command(client: Client, message: Message):
    """Authorize current group"""
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("❌ This command can only be used in groups.")
        return
    
    bot_data.authorize_group(message.chat.id)
    await message.reply_text(f"✅ This group has been authorized!")

@app.on_message(filters.command("revokegroup") & filters.user(OWNER_ID))
async def revokegroup_command(client: Client, message: Message):
    """Revoke group authorization"""
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("❌ This command can only be used in groups.")
        return
    
    bot_data.revoke_group(message.chat.id)
    await message.reply_text(f"✅ This group's authorization has been revoked.")

@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_command(client: Client, message: Message):
    """Ban a user"""
    try:
        user_id = int(message.text.split()[1])
        bot_data.ban_user(user_id)
        await message.reply_text(f"✅ User `{user_id}` has been banned.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: `/ban <user_id>`")

@app.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_command(client: Client, message: Message):
    """Unban a user"""
    try:
        user_id = int(message.text.split()[1])
        bot_data.unban_user(user_id)
        await message.reply_text(f"✅ User `{user_id}` has been unbanned.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: `/unban <user_id>`")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_command(client: Client, message: Message):
    """Broadcast message to all authorized users"""
    msg_text = message.text.split(maxsplit=1)
    if len(msg_text) < 2:
        await message.reply_text("Usage: `/broadcast <message>`")
        return
    
    broadcast_text = msg_text[1]
    users = bot_data.data['authorized_users']
    
    success = 0
    failed = 0
    
    status_msg = await message.reply_text("📢 Broadcasting message...")
    
    for user_id in users:
        try:
            await client.send_message(user_id, f"📢 **Broadcast Message**\n\n{broadcast_text}")
            success += 1
        except Exception as e:
            logger.error(f"Failed to send to {user_id}: {e}")
            failed += 1
    
    await status_msg.edit_text(
        f"✅ Broadcast complete!\n\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

# Inline query handler
@app.on_inline_query()
async def inline_query_handler(client: Client, inline_query: InlineQuery):
    """Handle inline queries"""
    user_id = inline_query.from_user.id
    
    if not bot_data.is_user_authorized(user_id):
        await inline_query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="❌ Unauthorized - Click to authorize",
            switch_pm_parameter="start"
        )
        return
    
    query = inline_query.query.strip()
    
    if not query:
        await inline_query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="💭 Type your question...",
            switch_pm_parameter="help"
        )
        return
    
    # Get user's model
    model = bot_data.get_user_model(user_id)
    
    try:
        # Call OpenAI API
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Provide clear and concise responses suitable for inline messaging."},
            {"role": "user", "content": query}
        ]
        
        response, tokens = await call_openai_api(messages, model, max_tokens=500)
        
        # Log usage
        bot_data.log_usage(user_id, model, tokens)
        
        # Create result
        result = InlineQueryResultArticle(
            title=f"🤖 AI Response ({model})",
            description=response[:100] + "..." if len(response) > 100 else response,
            input_message_content=InputTextMessageContent(
                message_text=f"{response}\n\n━━━━━━━━━━━━━━━\n🤖 {model} | 🎯 {tokens} tokens"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 Ask Another", switch_inline_query_current_chat="")
            ]])
        )
        
        await inline_query.answer(
            results=[result],
            cache_time=0
        )
        
    except Exception as e:
        logger.error(f"Inline query error: {e}")
        error_result = InlineQueryResultArticle(
            title="❌ Error",
            description=str(e),
            input_message_content=InputTextMessageContent(
                message_text=f"❌ Error: {str(e)}"
            )
        )
        await inline_query.answer(results=[error_result], cache_time=0)

# Callback query handler
@app.on_callback_query()
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    """Handle callback queries"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if not bot_data.is_user_authorized(user_id):
        await callback_query.answer("❌ Unauthorized access.", show_alert=True)
        return
    
    if data == "change_model":
        current_model = bot_data.get_user_model(user_id)
        text = f"**🤖 Select Your AI Model**\n\nCurrent: `{current_model}`"
        await callback_query.message.edit_text(
            text,
            reply_markup=create_model_keyboard()
        )
    
    elif data.startswith("model_"):
        model = data.replace("model_", "")
        bot_data.set_user_model(user_id, model)
        await callback_query.answer(f"✅ Model changed to {model}", show_alert=True)
        await callback_query.message.edit_text(
            f"✅ **Model Updated!**\n\nYour default model is now: `{model}`\n\n"
            f"{AVAILABLE_MODELS.get(model, model)}",
            reply_markup=create_main_menu()
        )
    
    elif data == "stats":
        stats = bot_data.data['usage_stats'].get(str(user_id))
        
        if not stats:
            await callback_query.answer("No statistics available yet.", show_alert=True)
            return
        
        text = "📊 **Your Usage Statistics**\n\n"
        text += f"🔢 Total Requests: `{stats['total_requests']}`\n"
        text += f"🎯 Total Tokens: `{stats['total_tokens']:,}`\n\n"
        text += "**By Model:**\n"
        
        for model, data in stats['by_model'].items():
            text += f"• `{model}`: {data['requests']} requests\n"
        
        await callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("« Back", callback_data="back_to_menu")
            ]])
        )
    
    elif data == "help":
        help_text = "📚 **Quick Help**\n\n"
        help_text += "• Use /ask to ask questions\n"
        help_text += "• Use /model to change AI model\n"
        help_text += "• Use inline mode for quick queries\n"
        help_text += "• Use /help for detailed instructions"
        
        await callback_query.message.edit_text(
            help_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("« Back", callback_data="back_to_menu")
            ]])
        )
    
    elif data == "back_to_menu":
        await callback_query.message.edit_text(
            "🤖 **Main Menu**\n\nSelect an option:",
            reply_markup=create_main_menu()
        )
    
    await callback_query.answer()

# Direct message handler (for natural conversation)
@app.on_message(filters.text & filters.private & ~filters.command([
    "start", "ask", "model", "stats", "help", "auth", "revoke",
    "authgroup", "revokegroup", "ban", "unban", "broadcast"
]))
async def natural_conversation_handler(client: Client, message: Message):
    """Handle natural conversation in private chats"""
    user_id = message.from_user.id
    
    if not bot_data.is_user_authorized(user_id):
        await message.reply_text("❌ You are not authorized to use this bot.")
        return
    
    # Get user's model preference
    model = bot_data.get_user_model(user_id)
    
    # Send typing action
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    
    try:
        # Call OpenAI API
        messages = [
            {"role": "system", "content": "You are a friendly and helpful AI assistant. Engage in natural conversation."},
            {"role": "user", "content": message.text}
        ]
        
        response, tokens = await call_openai_api(messages, model)
        
        # Log usage
        bot_data.log_usage(user_id, model, tokens)
        
        await message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error in natural conversation: {e}")
        await message.reply_text(
            f"❌ Sorry, an error occurred: `{str(e)}`"
        )

if __name__ == "__main__":
    logger.info("Starting Advanced AI Assistant Bot...")
    app.run()
