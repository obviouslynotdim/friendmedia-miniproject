# Portfolio & Friend Manager

This is a Flask-based web application that allows users to register, manage their personal account, and maintain a collection of **Friend Profiles**. The application features user authentication, profile image processing, and a relational database to link profiles to specific users.

---

## 🚀 Features

* **User Authentication**: Secure registration and login system using `Flask-Login` and password hashing with `Bcrypt`.
* **Account Management**: Users can update their full name and upload a custom profile avatar.
* **Friend Profiles**: Create and store profiles for friends, including their name, role, bio, and a profile picture.
* **Image Processing**: Automatic resizing and renaming of uploaded images using the `Pillow` library.
* **Database Integration**: Uses `Flask-SQLAlchemy` with a SQLite backend to manage one-to-many relationships between users and their friend entries.

---

## 🛠️ Technology Stack

| Component | Technology |
| --- | --- |
| **Backend** | Python, Flask |
| **Database** | SQLAlchemy (SQLite) |
| **Auth** | Flask-Login, Flask-Bcrypt |
| **Forms** | Flask-WTF, WTForms |
| **Imaging** | Pillow (PIL) |

---

## 📂 Project Structure

* `server.py`: The entry point for running the application.
* `portfo/`: The main package containing the app logic.
* `__init__.py`: App initialization and extension configuration.
* `models.py`: SQLAlchemy database models for `User` and `FriendProfile`.
* `routes.py`: View functions and URL routing.
* `forms.py`: WTForms definitions for registration, login, and profile updates.


* `requirements.txt`: List of Python dependencies.

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd <repo-name>

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Initialize the Database**:
Open a Python shell and run:
```python
from portfo import app, db
with app.app_context():
    db.create_all()

```


4. **Run the application**:
```bash
python server.py

```


The app will be available at `http://127.0.0.1:5000`.

