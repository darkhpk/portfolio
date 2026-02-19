#!/bin/bash

# Online Classroom - Log Viewer
# Quick utility to view application logs

echo "========================================"
echo " Online Classroom - Log Viewer"
echo "========================================"
echo ""

LOG_DIR="w_classroom/logs"

if [ ! -d "$LOG_DIR" ]; then
    echo "Error: Logs directory not found at $LOG_DIR"
    exit 1
fi

# Function to view a specific log file
view_log() {
    local logfile="$LOG_DIR/$1"
    if [ -f "$logfile" ]; then
        echo "Viewing: $1"
        echo "========================================"
        tail -n 50 "$logfile"
        echo ""
        echo "To follow in real-time: tail -f $logfile"
    else
        echo "Log file not found: $1"
    fi
}

# Menu
echo "Available logs:"
echo "  1. Django (general application logs)"
echo "  2. Errors (error logs only)"
echo "  3. WebSocket (connection logs)"
echo "  4. Code Execution (code execution logs)"
echo "  5. View all recent logs"
echo "  6. Clear all logs"
echo ""
read -p "Select option (1-6): " choice

case $choice in
    1)
        view_log "django.log"
        ;;
    2)
        view_log "errors.log"
        ;;
    3)
        view_log "websocket.log"
        ;;
    4)
        view_log "code_execution.log"
        ;;
    5)
        echo "=== Django Log ==="
        view_log "django.log"
        echo ""
        echo "=== Error Log ==="
        view_log "errors.log"
        echo ""
        echo "=== WebSocket Log ==="
        view_log "websocket.log"
        echo ""
        echo "=== Code Execution Log ==="
        view_log "code_execution.log"
        ;;
    6)
        read -p "Are you sure you want to clear all logs? (y/n): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            rm -f "$LOG_DIR"/*.log
            echo "All logs cleared."
        else
            echo "Cancelled."
        fi
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "Log files location: $LOG_DIR"
echo "========================================"
