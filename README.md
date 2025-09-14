# sql-project
🚉 Railway Management System
📌 Overview

This is a console-based Railway Management System built using Python and MySQL.
It allows users to:

Create and manage their accounts

Book train tickets and get a unique PNR number

View their booked tickets

Check live PNR Status through an external API from RapidAPI

This project is designed for learning and demonstration purposes.

⚡ Features

User Registration & Login

Book Train Tickets (with auto-generated PNR)

View Booked Tickets

Check Live PNR Status using RapidAPI

Persistent Storage using MySQL Database

⚙️ Requirements

Python 3.x

MySQL Server

Python modules:

pip install mysql-connector-python requests


RapidAPI account (for PNR Status API)

API: IRCTC Indian Railway PNR Status

Get your API key from RapidAPI

⚡ How It Works

Database Setup

When you run the program, it first asks for your MySQL host, username, and password.
It automatically creates a database named IRCTC and sets up the required tables if they don’t exist.

User Management

New users can create an account by entering details like name, gender, age, DOB, and phone number.
A unique user ID is generated automatically and stored in the database.
Existing users can log in using their user ID and password.

Ticket Booking

After login, the user can book tickets by providing the train name, journey date, from station, and to station.
The system automatically generates a 10-digit PNR number for each booking and saves the details in the database.

View Tickets

Users can view all the tickets they have booked, along with details like PNR, train name, journey date, and route.

PNR Status (Live)

* Users can check the live status of any PNR.
* The system sends a request to the RapidAPI IRCTC PNR Status API, retrieves the current status, and displays information such as:
* Train name and date of journey
* Chart preparation status
* Booking and current status of each passenger

Logout
Users can log out anytime and safely end their session.

▶️ How to Run

Make sure MySQL server is running on your machine.
Clone or download this repository to your local system.
Open a terminal inside the project folder.
Run the script:

python railway\ management\ database.py

Enter your MySQL credentials and start using the system.

🌐 API Integration

The project uses RapidAPI to fetch live PNR Status.

You must insert your RapidAPI key in the code:

"X-RapidAPI-Key":"YOUR_API_KEY_HERE"
Replace "YOUR_API_KEY_HERE" with your actual API key
