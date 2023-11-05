# ZHA_Mailing

ZHA_Mailing is a Python project designed for sending messages to both chats and users via the Telegram API. It utilizes the `aiogram` library for handling commands and messages. Below are the instructions and details for setting up and using the project.

## Getting Started

### Prerequisites

- Python 3.6+
- PostgreSQL database

### Migrations

1. Install Alembic:

   ```
   pip install alembic
   ```

2. Initialize Alembic:

   ```
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

1. Clone the repository:

   ```
   git clone <repository-url>
   cd ZHA_Mailing
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database and configure the connection URL in `main.py`:

   ```
   postgresql+asyncpg://username:password@localhost:5432/db
   ```

4. Update the authentication token in `main.py`:

   ```python
   TOKEN = 'your_telegram_bot_token'
   ```

5. Run the project:

   ```
   python main.py
   ```

## Usage

### Commands

- `/add`: Start the process of adding a new case. You will be prompted for the recipient type (chat or users), name, photo (optional), and text.

- `/case <case_id>`: Retrieve information about a specific case, including participants who responded "No" along with their reasons.


## Detailed Migration Guide

For detailed information on how to perform migrations using Alembic, refer to the following blog post: [Connect to PostgreSQL with SQLAlchemy and asyncio](https://makimo.com/blog/connect-to-postgresql-with-sqlalchemy-and-asyncio/)

## Handlers

### Main Bot Handlers

The project contains various message handlers implemented in the `main.py` file under the `router` object. These handlers process different commands and messages, including adding cases, managing participants, and generating case reports.

### Poll State Handlers

The bot also includes state machine handlers implemented in the `main.py` file under the `router` object. These handlers guide users through a survey process, collecting information about their opinions and preferences.

## Additional Code

Additionally, there is a section of code provided for handling bot events, such as when the bot is added to a new chat as a member.

Feel free to customize and use the project according to your needs! If you have any questions or need further assistance, please don't hesitate to reach out.