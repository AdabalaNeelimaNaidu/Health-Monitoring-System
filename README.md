# Health Monitoring System

## Overview

This is a simple Health Monitoring System built using Python and Tkinter, with a SQLite database to store user and BMI data. It allows users to track their Body Mass Index (BMI) by entering their height and weight, view their BMI records, and provides registration and login functionality for both regular users and administrators.

Administrators can access users' health details, while regular users can calculate and store their BMI records and track their health progress.

## Features

### User Features:
- **User Registration**: Users can register with a username, password, email, and phone number.
- **User Login**: Registered users can log in using their credentials.
- **BMI Calculation**: Users can input their height and weight to calculate their BMI.
- **BMI Records**: After calculation, users' BMI records are saved in a database and displayed in their health history.
- **Logout**: Users can log out to return to the home page.

### Admin Features:
- **Admin Registration**: Administrators can register with a username, password, email, and phone number.
- **Admin Login**: Admins can log in using their credentials.
- **View Users' Health Details**: Admins can fetch and view BMI records of any user by entering their username.
  
### Additional Features:
- **Documentation**: The system includes a documentation page to explain how the system works.
  
## Technologies Used
- **Python**: The system is implemented using Python programming language.
- **Tkinter**: Tkinter is used for the graphical user interface (GUI).
- **SQLite**: SQLite is used as the database to store users, administrators, and BMI records.

## Requirements
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- SQLite3 (comes pre-installed with Python)

## Installation

1. Clone or download the repository to your local machine.
2. Navigate to the project directory.
3. Ensure you have Python 3.x installed.
4. Run the following command to install any dependencies:
   ```bash
   pip install -r requirements.txt
5. Run the application
   ```bash
   python health_monitoring_system.py





