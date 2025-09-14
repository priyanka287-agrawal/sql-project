# RAILWAY MANAGEMENT SYSTEM

# Importing Modules
import mysql.connector as sql
from random import randint
import requests

# --- Fetch PNR Status ---
def fetch_pnr_status(pnr):
    url = "https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnrNumber}"

    params = {"pnrNumber": str(pnr)}
    headers = {
        "X-RapidAPI-Key": "052e64e593mshcc66e339fa2889cp1ec8e8jsnb11486d1bf39",   # paste your API key here
        "X-RapidAPI-Host": "irctc-indian-railway-pnr-status.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


# Establishment of connection to MySQL Server
print("Enter the details of your MySQL Server:")
x = input("Hostname: ")
y = input("User: ")
z = input("Password: ")

con = sql.connect(host=x, user=y, password=z)
con.autocommit = True
cur = con.cursor()

# Create database and tables if not exist
cur.execute("CREATE DATABASE IF NOT EXISTS IRCTC;")
cur.execute("USE IRCTC;")

cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY,
    pass VARCHAR(16),
    name VARCHAR(100),
    sex CHAR(1),
    age INT,
    dob DATE,
    ph_no VARCHAR(15)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INT PRIMARY KEY,
    pnr VARCHAR(12) NOT NULL,
    train VARCHAR(25),
    doj DATE,
    tfr VARCHAR(100),
    tto VARCHAR(100),
    FOREIGN KEY (id) REFERENCES accounts(id)
);
""")

# ------------------ FUNCTIONS ------------------

# Login Menu
def login_menu():
    print("\nWELCOME TO THE IRCTC PORTAL")
    print("1. Create New Account \n2. Log In \n3. Exit")
    opt = int(input("Enter your choice: "))
    if opt == 1:
        create_acc()
    elif opt == 2:
        login()
    elif opt==3:
        print("goodbye!")

    else:
        e = input("Exit the portal? (Y/N) ")
        if e.upper() == "N":
            login_menu()

# Account Creation
def create_acc():
    print("\nEnter the details to create your account:")
    i = randint(1000, 9999)
    print(f"Your generated ID is: {i}")
    p = input("Enter your password: ")
    n = input("Enter your name: ")
    sex = input("Enter your gender (M/F/O): ")
    age = int(input("Enter your age: "))
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    ph = input("Enter your contact number: ")

    cur.execute(
        "INSERT INTO accounts VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (i, p, n, sex.upper(), age, dob, ph)
    )

    print("Account created successfully! Now log in.")
    login()

# Login
def login():
    print("\n--- LOGIN ---")
    uid = int(input("Enter User ID: "))
    pw = input("Enter Password: ")

    cur.execute("SELECT * FROM accounts WHERE id=%s AND pass=%s", (uid, pw))
    user = cur.fetchone()

    if user:
        print(f"\nWelcome back, {user[2]}!")
        user_menu(uid)
    else:
        print("Invalid ID or Password. Try again.")
        login_menu()

# User Menu after login
def user_menu(uid):
    while True:
        print("\n--- USER MENU ---")
        print("1. Book Ticket\n2. View My Tickets\n3. Pnr status\n4. Logout")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            book_ticket(uid)
        elif choice == 2:
            view_tickets(uid)
        elif choice== 3:
            check_pnr()
        elif choice == 4:
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

# Ticket Booking
def book_ticket(uid):
    print("\nEnter ticket details:")
    train = input("Train name: ")
    doj = input("Date of journey (YYYY-MM-DD): ")
    tfr = input("From station: ")
    tto = input("To station: ")

    pnr =str(randint(1000000000, 9999999999) ) # 10-digit PNR
    cur.execute(
        "INSERT INTO tickets VALUES (%s, %s, %s, %s, %s, %s)",
        (uid, pnr, train, doj, tfr, tto)
    )
    con.commit()
    print(f"Ticket booked successfully! Your PNR is {pnr}")

# View Tickets
def view_tickets(uid):
    cur.execute("SELECT * FROM tickets WHERE id=%s", (uid,))
    tickets = cur.fetchall()

    if not tickets:
        print("No tickets booked yet.")
    else:
        print("\nYour Tickets:")
        for t in tickets:
            print(f"PNR: {t[1]}, Train: {t[2]}, DOJ: {t[3]}, From: {t[4]}, To: {t[5]}")
# Check PNR Status
# Check PNR Status
def check_pnr():
    pnr = input("Enter your PNR number: ")
    data = fetch_pnr_status(pnr)

    print("\n📌 PNR Status Data (Raw):")
    print(data)

    if "data" in data:
        train = data["data"].get("train", "Unknown")
        doj = data["data"].get("doj", "Unknown")
        chart = data["data"].get("chartPrepared", "Unknown")

        print(f"\n🚆 Train: {train}")
        print(f"📅 Date of Journey: {doj}")
        print(f"📊 Chart Prepared: {chart}")

        passenger_list = data["data"].get("passengerList", [])
        if passenger_list:
            for idx, passenger in enumerate(passenger_list, start=1):
                print(f"\n👤 Passenger {idx}:")
                print(f"   Booking Status: {passenger.get('bookingStatus', 'N/A')}")
                print(f"   Current Status: {passenger.get('currentStatus', 'N/A')}")
        else:
            print("\n⚠️ No passenger details available.")
    else:
        print("\n❌ Invalid response from API.")

# ------------------ RUN SYSTEM ------------------
login_menu()
