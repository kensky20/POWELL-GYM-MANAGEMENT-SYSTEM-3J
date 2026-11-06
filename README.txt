POWELL POWER WELLNESS GYM - MEMBERSHIP RECORD MANAGEMENT SYSTEM

TECHNOLOGY
Python 3 + Tkinter GUI + Python built-in HTTP API + JSON file storage.
No SQL, MySQL, PHP, XAMPP, or Flask. No payment and no biometrics.

FILES
main.py                 Starts API and login window.
login.py                Login interface.
gym_system.py           Dashboard and membership CRUD GUI.
api.py                  Python HTTP API (GET, POST, PUT, DELETE).
database.py             JSON database functions.
test_system.py          Automated unit tests.
powell_gym_data.json    Member records (created automatically).
users.json              Login accounts (created automatically).

RUN THE SYSTEM
1. Install Python 3. During installation, check "Add Python to PATH".
2. Open this folder in VS Code.
3. Open Terminal > New Terminal.
4. Run: python main.py
5. Login:
   Username: admin
   Password: admin123

RUN TESTS
In VS Code terminal, run:
python -m unittest test_system.py

TESTING CHECKLIST
- Login: correct and incorrect credentials.
- Add: save a valid member; reject invalid or empty fields.
- View: confirm member appears in the table.
- Search: search by name and member ID.
- Update: select a row, edit details, and save.
- Delete: confirm deletion and test Cancel.
- API: check GET /health and CRUD requests.
- JSON persistence: close and reopen; confirm saved members remain.

MEMBER DATA FIELDS
Full name, age, gender, contact number, address, membership type,
start date, expiration date, automatic member ID, and membership status.

VALIDATION
Age: 1-120. Contact: 11-digit Philippine mobile number 09XXXXXXXXX.
Dates: YYYY-MM-DD. Expiration date cannot be earlier than start date.
Membership type: Daily, Weekly, Monthly, Quarterly, or Yearly.

IMPORTANT
The default classroom login is stored in users.json as plain text.
Change it before using real information and do not reuse an important password.
The API listens only on this computer (127.0.0.1), not on the public internet.
The API starts automatically with main.py. Do not start api.py separately.
Back up both JSON files regularly.
