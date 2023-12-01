# ZHA_Mailing

ZHA_Mailing is a Python project designed for sending messages to both chats and users via the Telegram API. It utilizes the `aiogram` library for handling commands and messages. Below are the instructions and details for setting up and using the project.

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database

### Migrations



1. Install Requirements:

   ```
   pip install sqlalchemy[asyncio]
   pip install "fastapi[all]"
   pip install -U aiogram
   pip install alembic
   ```

   you should create db in psql 
   CREATE DATABASE new_people_db or another and change it in config url

2. Initialize Alembic:

   ```
   git clone https://github.com/SalaFanChik/new_people/
   cd new_people
   alembic init -t async alembic
   ```

3. Generate a new migration file:

   ```
   alembic revision --autogenerate -m "Add Tutorial model"
   ```

4. Apply the migration:

   ```
   alembic upgrade head
   ```


### Installation

1. Update the authentication token in `main.py`:

   ```python
   TOKEN = 'your_telegram_bot_token'
   ```

2. install ngrok and run ngrok http 8000

   ```python
   NGROK_URL = "your url"
   ```
3. Run the project:

   ```
   python main.py
   ```

## Usage

### Commands

- `/add`: Start the process of adding a new case. You will be prompted for the recipient type (chat or users), name, photo (optional), and text.

- `/case <case_id>`: Retrieve information about a specific case, including participants who responded "No" along with their reasons.

- other see in code 
## Detailed Migration Guide

For detailed information on how to perform migrations using Alembic, refer to the following blog post: [Connect to PostgreSQL with SQLAlchemy and asyncio](https://makimo.com/blog/connect-to-postgresql-with-sqlalchemy-and-asyncio/)
