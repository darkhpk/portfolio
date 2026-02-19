#!/bin/bash

echo "Starting Online Classroom Server..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Navigate to project directory
cd w_classroom

# Start server
echo "Server starting at http://0.0.0.0:8000/"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver 0.0.0.0:8000
