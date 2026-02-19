# 🎓 Online Classroom - Collaborative Code Editor

A real-time collaborative code editor built with Django and WebSockets. Multiple users can code together, execute code in various languages, and see results instantly.

## ✨ Features

- 👥 **Real-time Collaboration**: Multiple users can edit code simultaneously with WebSocket-based synchronization
- 🏠 **Lobby System**: Create and join coding rooms with participant tracking
- 💻 **Multi-Language Support**: Python, JavaScript, Java, C++, and C
- 🚀 **Live Code Execution**: Run code directly and see results in real-time
- 📝 **Line Numbers**: Professional code editor with line numbering
- 🎨 **Modern UI**: Split-screen interface with dark theme
- 👥 **Participant Tracking**: See who's online in your room
- 📋 **Code Management**: Copy, clear, and manage code easily

## 🚀 Quick Start

### Windows (Local Development)
```bash
# Run the automated setup
setup.bat

# Start the server
start_server.bat
```

### Linux / VPS
```bash
# Make scripts executable
chmod +x setup.sh start_server.sh

# Run the setup
./setup.sh

# Start the server
./start_server.sh
```

Visit **http://localhost:8000** to get started!

## 📋 Requirements

### Core Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Optional (for code execution)
- Node.js (for JavaScript)
- Java JDK 11+ (for Java)
- GCC/G++ (for C/C++)

## 🔧 Manual Installation

1. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   cd w_classroom
   python manage.py migrate
   ```

4. **Start development server**
   ```bash
   python manage.py runserver

   # For VPS (accessible externally)
   python manage.py runserver 0.0.0.0:8000
   ```

## 📖 Usage

### Creating a Room
1. Visit the lobby (homepage)
2. Enter your name and a room name
3. Click "Create Room"
4. Share the room URL with collaborators

### Joining a Room
1. Click "Join" on any active room in the lobby
2. Enter your name
3. Start coding together!

### Coding Together
1. Select programming language from dropdown
2. Write code in the editor (with line numbers!)
3. Click "Run" to execute (or press Ctrl/Cmd + Enter)
4. View output in the right panel
5. See other participants in the dropdown menu

### Control Buttons
- **▶ Run**: Execute the current code
- **Clear Code**: Remove all code from the editor
- **Clear Output**: Clear the output panel
- **Copy Code**: Copy code to clipboard

## 🌐 Production Deployment

For VPS or cloud deployment, see **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions on:
- Setting up with Nginx + Gunicorn/Daphne
- Configuring SSL with Let's Encrypt
- Using Redis for WebSocket channels
- Docker deployment
- Security hardening

## 💻 Language Requirements

To execute code in different languages, ensure the following are installed:

### Linux/Ubuntu
```bash
sudo apt install nodejs default-jdk gcc g++
```

### CentOS/RHEL
```bash
sudo yum install nodejs java-11-openjdk-devel gcc gcc-c++
```

### macOS
```bash
brew install node openjdk gcc
```

### Windows
- **Python**: Included with Django
- **JavaScript**: Install [Node.js](https://nodejs.org/)
- **Java**: Install [JDK](https://www.oracle.com/java/technologies/downloads/)
- **C/C++**: Install [MinGW](https://www.mingw-w64.org/) or Visual Studio

## 📁 Project Structure

```
web classroom/
├── w_classroom/              # Django project
│   ├── classroom/           # Main application
│   │   ├── static/css/     # Stylesheets
│   │   ├── templates/      # HTML templates
│   │   ├── models.py       # Database models
│   │   ├── views.py        # HTTP views
│   │   ├── consumers.py    # WebSocket handlers
│   │   └── executor.py     # Code execution engine
│   ├── w_classroom/        # Project settings
│   ├── logs/              # Application logs
│   └── manage.py           # Django management
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
├── setup.sh               # Linux setup script
├── start_server.bat       # Windows start script
├── start_server.sh        # Linux start script
├── view_logs.bat          # Windows log viewer
├── view_logs.sh           # Linux log viewer
├── DEPLOYMENT.md          # Production deployment guide
└── README.md              # This file
```

## 📊 Logging

The application includes comprehensive logging to help with debugging and monitoring:

### Log Files (in `w_classroom/logs/`)
- **django.log** - General application logs
- **errors.log** - Error logs only
- **websocket.log** - WebSocket connection logs
- **code_execution.log** - Code execution logs

### View Logs
```bash
# Windows
view_logs.bat

# Linux
chmod +x view_logs.sh
./view_logs.sh
```

### Manual Log Access
```bash
# View last 50 lines
tail -n 50 w_classroom/logs/django.log

# Follow logs in real-time
tail -f w_classroom/logs/websocket.log
```

## 🛠️ Tech Stack

- **Backend**: Django 5.0 + Django Channels 4.0
- **WebSockets**: Daphne ASGI Server
- **Frontend**: Vanilla JavaScript + CSS
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Real-time**: WebSocket protocol

## ⚠️ Security Notes

**Important**: This application executes user-submitted code on the server.

### For Development
- Only use on trusted networks
- Default setup is safe for local/trusted use

### For Production
See [DEPLOYMENT.md](DEPLOYMENT.md) for security hardening:
- Run code in isolated containers (Docker)
- Implement authentication and authorization
- Add rate limiting
- Use Redis for Channels layer
- Set strict resource limits
- Enable HTTPS/SSL
- Configure firewall rules
- Validate and sanitize all inputs

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -ti:8000 | xargs kill -9
```

### WebSocket Connection Failed
- Verify Daphne is running
- Check firewall settings
- For VPS: Allow port 8000 in security groups

### Code Execution Not Working
- Install required language compilers/runtimes
- Check PATH environment variables
- Verify permissions on Linux/macOS

### Static Files Not Loading
```bash
cd w_classroom
python manage.py collectstatic
```

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Happy Coding! 🚀**

## Development

The project structure:
```
web classroom/
├── manage.py
├── requirements.txt
├── README.md
├── web_classroom/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── classroom/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── consumers.py
    ├── routing.py
    ├── executor.py
    └── templates/
        └── classroom/
            ├── classroom.html
            └── redirect.html
```

## License

This project is provided as-is for educational purposes.
