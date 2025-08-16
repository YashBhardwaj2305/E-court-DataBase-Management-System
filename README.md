🏛️ E-Court Database Management System

A Flask-based web application for managing and searching legal case records.
It provides functionalities for case registration, updates, and search using multiple parameters (CNR number, FIR number, Case number, Status ID, File name).

✨ Features

👤 Role-based access:

Head login (adminhead@gmail.com / adminhead) – can register new Admins.

Admin login – registered by Head.

User login – regular case search/registration.

📂 Case Management:

Register new cases with details (Prosecutor, Police Station, Court, Acts, Sections, Witnesses).

Update existing cases.

View details using CNR, Case No, FIR No, Status ID, or File Name.

📊 Database:

SQLite (site.db) with SQLAlchemy ORM.

Well-structured models for all case-related entities.

⚙️ Setup & Installation
1. Clone the Repository
git clone https://github.com/YashBhardwaj2305/E-court-DataBase-Management-System.git
cd E-court-DataBase-Management-System

2. Create Virtual Environment
python -m venv venv


Activate it:

Windows (PowerShell)

.\venv\Scripts\Activate.ps1


Windows (CMD)

venv\Scripts\activate.bat


Linux / Mac

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Initialize Database
python

from routes import db
db.create_all()
exit()

5. Run the App
$env:FLASK_APP = "routes.py"
$env:FLASK_ENV = "development"
flask run


Go to: 👉 http://127.0.0.1:5000/

🗂️ Project Structure
├── application/         # Database + models
│   ├── database.py
│   ├── models.py
├── templates/           # HTML templates
├── static/              # CSS, JS, Images
├── routes.py            # Flask routes & app setup
├── site.db              # SQLite database (auto-created)
├── requirements.txt     # Dependencies
├── .gitignore
└── README.md

👨‍⚖️ Default Credentials

Head:

Email: adminhead@gmail.com

Password: adminhead

Admins and Users can be created via the interface.

🚀 Future Enhancements

Add password hashing for security.

Add case status tracking dashboard.

Improve UI with Bootstrap/Tailwind.

Deploy on Render/Heroku for public access.
