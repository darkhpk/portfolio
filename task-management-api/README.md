# Task Management API

A RESTful API built with FastAPI for managing tasks, projects, and user collaboration. Features JWT authentication, PostgreSQL database, and comprehensive API documentation.

## Features

- **RESTful API Design**: Clean and intuitive endpoints
- **Authentication & Authorization**: JWT-based authentication
- **CRUD Operations**: Complete task and project management
- **User Management**: User registration, login, and profiles
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error handling and logging
- **Testing**: Unit and integration tests

## Technologies Used

- FastAPI - Modern web framework
- SQLAlchemy - ORM for database operations
- PostgreSQL - Database
- Pydantic - Data validation
- JWT - Authentication tokens
- Uvicorn - ASGI server
- pytest - Testing framework

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/taskdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Setup

```bash
# Initialize database
python init_db.py
```

## Usage

### Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info

### Tasks
- `GET /tasks` - List all tasks
- `GET /tasks/{id}` - Get specific task
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/status` - Update task status

### Projects
- `GET /projects` - List all projects
- `GET /projects/{id}` - Get specific project
- `POST /projects` - Create new project
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Users
- `GET /users` - List all users (admin only)
- `GET /users/{id}` - Get specific user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

## Example Usage

### Register a user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

### Create a task:
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete API", "description": "Finish the API implementation", "priority": "high"}'
```

## Project Structure

- `main.py` - Application entry point
- `init_db.py` - Database initialization
- `app/` - Application code
  - `api/` - API routes
  - `models/` - Database models
  - `schemas/` - Pydantic schemas
  - `core/` - Core functionality (auth, config)
  - `db/` - Database configuration

## Testing

```bash
pytest tests/
```

## Future Enhancements

- Task assignments and collaboration
- File attachments
- Task comments and activity logs
- Email notifications
- Webhooks
- Rate limiting
- Caching with Redis
