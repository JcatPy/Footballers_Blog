# Footballers Blog

Footballers Blog is a web application that allows users to share and explore posts about football players. The application includes user authentication, profile management, and blogging functionality. It is built with Flask and SQLite, making it lightweight and easy to set up.

## Features
- **Dynamic Footballer Profiles**: Displays a list of football players with their attributes like name, age, height, and country.
- **User Authentication**: Users can register, log in, and log out securely.
- **Blogging Platform**: Users can create, view, and manage posts.
- **Profile Management**: Users can update their profile information, including username and email.
- **Responsive Web Design**: Clean and user-friendly interface.

## Tech Stack
- **Frontend**: HTML, CSS, Bootstrap (for styling).
- **Backend**: Flask (Python).
- **Database**: SQLite (SQLAlchemy for ORM).
- **Libraries**:
  - Flask-WTF: Form handling.
  - Flask-Bcrypt: Password hashing.
  - Flask-Login: User session management.
  - Flask-SQLAlchemy: ORM for database operations.

## Prerequisites
- Python 3.x installed.
- A virtual environment setup.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/footballers-blog.git
cd footballers-blog
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Ensure the `FLASK_APP` variable is set to your application entry point:
```bash
export FLASK_APP=app.py  # On Windows, use set FLASK_APP=app.py
```

### 5. Setup Database
Open a Python shell and run:
```bash
python
```
```python
from app import db
db.create_all()
exit()
```

### 6. Run the Application
```bash
flask run
```
