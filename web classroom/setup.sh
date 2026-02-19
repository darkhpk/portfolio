#!/bin/bash

echo "========================================"
echo " Online Classroom - Linux Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo -e "${GREEN}[1/6] Checking Python version...${NC}"
python3 --version

echo ""
echo -e "${GREEN}[2/6] Installing system dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    echo "Detected Debian/Ubuntu system"
    sudo apt-get update
    sudo apt-get install -y python3-venv python3-dev build-essential gcc g++ default-jdk nodejs
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    echo "Detected CentOS/RHEL system"
    sudo yum install -y python3-devel gcc gcc-c++ java-11-openjdk-devel nodejs
elif command -v dnf &> /dev/null; then
    # Fedora
    echo "Detected Fedora system"
    sudo dnf install -y python3-devel gcc gcc-c++ java-11-openjdk-devel nodejs
else
    echo -e "${YELLOW}Warning: Could not detect package manager. Please install manually:${NC}"
    echo "  - Python 3 development headers"
    echo "  - GCC/G++ compilers"
    echo "  - Java JDK (for Java code execution)"
    echo "  - Node.js (for JavaScript code execution)"
fi

echo ""
echo -e "${GREEN}[3/6] Creating virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi

echo ""
echo -e "${GREEN}[4/6] Activating virtual environment...${NC}"
source .venv/bin/activate

echo ""
echo -e "${GREEN}[5/6] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo -e "${GREEN}[6/6] Running database migrations...${NC}"
cd w_classroom
python manage.py migrate
cd ..

echo ""
echo "========================================"
echo -e "${GREEN} Setup Complete!${NC}"
echo "========================================"
echo ""
echo "To start the development server:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Navigate to project: cd w_classroom"
echo "  3. Run server: python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Or simply run: ./start_server.sh"
echo ""
echo "For production deployment, see: DEPLOYMENT.md"
echo ""
