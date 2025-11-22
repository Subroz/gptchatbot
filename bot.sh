#!/bin/bash

# Bot Management Script

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BOT_SCRIPT="$SCRIPT_DIR/telegram_ai_bot.py"
PID_FILE="$SCRIPT_DIR/bot.pid"
LOG_FILE="$SCRIPT_DIR/bot.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

check_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

start_bot() {
    if check_running; then
        print_warning "Bot is already running (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    print_status "Starting bot..."
    
    # Check if .env exists
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        print_error ".env file not found!"
        print_warning "Please run ./setup.sh first or create .env manually"
        exit 1
    fi
    
    # Start bot in background
    cd "$SCRIPT_DIR"
    nohup python3 "$BOT_SCRIPT" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 2
    
    if check_running; then
        print_status "Bot started successfully (PID: $(cat $PID_FILE))"
        print_status "Logs: tail -f $LOG_FILE"
    else
        print_error "Failed to start bot. Check logs: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

stop_bot() {
    if ! check_running; then
        print_warning "Bot is not running"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    print_status "Stopping bot (PID: $PID)..."
    
    kill "$PID"
    sleep 2
    
    # Force kill if still running
    if ps -p "$PID" > /dev/null 2>&1; then
        print_warning "Forcing bot to stop..."
        kill -9 "$PID"
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    print_status "Bot stopped"
}

restart_bot() {
    print_status "Restarting bot..."
    stop_bot
    sleep 1
    start_bot
}

status_bot() {
    if check_running; then
        PID=$(cat "$PID_FILE")
        print_status "Bot is running (PID: $PID)"
        
        # Show resource usage
        echo ""
        echo "Resource Usage:"
        ps -p "$PID" -o pid,vsz,rss,pcpu,pmem,etime,cmd | tail -n 1
    else
        print_warning "Bot is not running"
    fi
}

show_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        print_error "Log file not found: $LOG_FILE"
        exit 1
    fi
    
    if [ "$1" == "-f" ] || [ "$1" == "--follow" ]; then
        tail -f "$LOG_FILE"
    else
        tail -n 50 "$LOG_FILE"
    fi
}

# Main script
case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        show_logs "$2"
        ;;
    *)
        echo "🤖 Advanced Telegram AI Bot - Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  status  - Check bot status"
        echo "  logs    - Show last 50 log lines"
        echo "  logs -f - Follow logs in real-time"
        echo ""
        exit 1
        ;;
esac

exit 0
