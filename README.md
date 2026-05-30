# TaskFlow SaaS Backend

Backend API for TaskFlow SaaS.

## Tech Stack

- Flask
- SQLAlchemy
- PostgreSQL (Supabase)
- Alembic
- Flask-Migrate
- JWT Authentication
- Flask-SocketIO

## Setup

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
python run.py
```

### Run Migrations

```bash
flask db migrate -m "message"
flask db upgrade
```

## Project

TaskFlow SaaS Assignment