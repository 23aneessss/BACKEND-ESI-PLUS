# Backend ESI+ 

ESI+ is a modern platform designed to support students in their daily study life. It provides tools such as todo management, a blog system, and an AI-powered chat assistant to help students stay organized, informed, and productive.


## Overview

This is a full-featured REST API backend built with FastAPI, providing user management, authentication, task tracking, blogging capabilities, and an integrated AI chatbot system.

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLAlchemy ORM with SQL database
- **Authentication:** JWT (JSON Web Tokens) with OAuth2
- **Password Hashing:** bcrypt
- **Validation:** Pydantic

## Project Structure

```
Backend-Projet-TEO/
├── main.py                 # Application entry point
├── database.py            # Database configuration and session management
├── models/                # SQLAlchemy database models
│   ├── user.py           # User model
│   ├── post.py           # Blog post model
│   ├── comment.py        # Comment model
│   ├── todo.py           # Todo/task model
│   └── convai.py         # AI conversation model
├── routers/               # API endpoints and routes
│   ├── auth.py           # Authentication endpoints (login, register)
│   ├── blog.py           # Blog post endpoints
│   ├── chat.py           # Chat/AI interaction endpoints
│   └── todo.py           # Todo management endpoints
└── schemas/               # Pydantic schemas for request/response validation
    ├── user.py           # User schema
    ├── post.py           # Post schema
    ├── comment.py        # Comment schema
    ├── chat.py           # Chat schema
    └── todo.py           # Todo schema
```

## Features

### 1. **Authentication System** (`/auth`)
- User registration with validation
- Email and username uniqueness checks
- JWT token-based authentication
- Secure password hashing with bcrypt
- Token refresh capabilities

### 2. **Todo Management** (`/todo`)
- Create, read, update, and delete tasks
- User-specific task lists
- Task status tracking

### 3. **Blog System** (`/blog`)
- Create and manage blog posts
- Comment functionality
- User attribution for posts and comments

### 4. **AI Chat** (`/chat`)
- Conversation management
- AI-powered chatbot integration
- Message history storage

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Backend-Projet-TEO
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY1=your_secret_key_here
   ALGORITHM1=HS256
   ```

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/` | Register a new user |
| POST | `/auth/token` | Login and get JWT token |
| GET/POST | `/todo/` | Get/create todos |
| GET/POST | `/blog/` | Get/create blog posts |
| POST | `/chat/` | Send message to AI chatbot |

## Authentication

The API uses JWT bearer token authentication. Include the token in request headers:

```
Authorization: Bearer <your_jwt_token>
```

## Database

The application uses SQLAlchemy ORM for database operations. Ensure your `DATABASE_URL` environment variable is correctly set to your database connection string.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Database connection string |
| `SECRET_KEY1` | Secret key for JWT signing |
| `ALGORITHM1` | JWT algorithm |
