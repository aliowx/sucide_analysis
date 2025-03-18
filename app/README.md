# 🚀 FastAPI Machine Learning API

This project is a FastAPI-based machine learning API that provides endpoints for model inference. The setup uses Poetry for dependency management and Alembic for database migrations.

## 🔧 Setup Project

### 📦 Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

If you are using Bash, add the following to your `~/.profile` or `~/.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

If you are using Fish, run:
```bash
fish_add_path $HOME/.local/bin
```

### 📂 Create Project Directory
```bash
cd backend
```

## ⚙️ Project Setup

### 🏗️ Create a New Project
```bash
poetry new app
```

### 📌 Install Dependencies
```bash
pip3 install uvicorn gunicorn fastapi
```
```bash
cd backend/app
```
```bash
poetry add fastapi uvicorn gunicorn pydantic numpy pandas scikit-learn joblib alembic sqlalchemy psycopg2
```

## 🔄 Initializing a Pre-existing Project
```bash
cd backend/app
```
```bash
poetry shell
```
```bash
poetry install
```

## 🗄️ Database Migration

### 📜 Create Migration File
```bash
alembic revision --autogenerate -m "Initial migration"
```

### 📥 Apply Migration
```bash
alembic upgrade head
```

## 🌍 Environment Variables
Create a `.env` file in `backend/app` and fill it with values from `.env.example`.

## 🔑 Create Superuser
Set user email and password in `.env`:
```ini
FIRST_SUPERUSER=
FIRST_SUPERUSER_PASSWORD=
```
Then, create the first superuser:
```bash
python3 initial_data.py
# or
poetry run python3 initial_data.py
```

## 🛰️ Test WebSocket
To test WebSocket, use the following endpoint:
```bash
ws://ip:port/api/v1/utils/echo-client/
```
Paste the response in an HTML file and open it in a browser.

## 🚀 Running the Project
To start the FastAPI server, run:
```bash
uvicorn app.main:app --reload
```

## 📑 Access API Documentation
- 📄 Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📘 Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


