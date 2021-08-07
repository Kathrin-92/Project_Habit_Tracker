"""
This document organises the basic functionality of our database and creates it if it does not already exist.
Furthermore, this code deals with the creation of a user profile (registration)
as well as with the login incl. password check.
For this it imports User.py to be able to use the UserClass.
It also imports the libraries questionary, sqlite3 and hashlib.
"""
import questionary
import sqlite3
import hashlib
import User


# THIS PART LAUNCHES THE DATABASE IF IT NOT ALREADY EXISTS.
# THE DATABASE CONSISTS OF THREE TABLES:
# USERS (FOR ALL USER DATA), HABITS (FOR ALL HABITS ACROSS USERS) & PROGRESS (FOR ALL PROGRESS DATA ACROSS USERS).
def launch_database():
    """
    Launch of the database if it not already exists.

    The database consists of three tables:
    * users --> for all user data
    * habits --> for all habits across all users
    * progress --> for all progress data across users
    """
    from os.path import join, dirname, abspath
    db_path = join(dirname(abspath(__file__)), 'main_db.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
              firstname text,
              lastname text,
              username text PRIMARY KEY,
              password text
              )""")

    c.execute("""CREATE TABLE IF NOT EXISTS habits (
                  habit_name text,
                  owner text, 
                  category text,
                  periodicity text,
                  datetime_of_creation datetime
                  )""")

    c.execute("""CREATE TABLE IF NOT EXISTS progress (
                  habit_name text,
                  periodicity text, 
                  owner text, 
                  datetime_of_completion datetime
                  )""")
    conn.commit()
    conn.close()


# THIS SECTION IS FOR THE SETUP OF FIRST TIME USERS.
# THE USER CAN ENTER THEIR FIRST AND LAST NAME, THEIR USERNAME AND THEIR PASSWORD.
# THE CODE CHECKS IF THE USERNAME ALREADY EXISTS AS THIS IS THE PRIMARY KEY AND CAN ONLY BE USED ONCE.
# THE CODE IS THEN SAVED IN THE DB.
def register_user():
    """
    Used for the user registration.

    A user is prompted to enter their first and last name, their username and password. The input is checked if it
    contains the right values.
    A new user is created and the data is saved in the database, if the username not already exists.
    A username can only exists once. If the username already exists, the user is prompted again to choose another
    username.
    """
    firstname = questionary.text("What is your first name? ",
                                 validate=lambda text: True if len(text) > 0 and text.isalpha()
                                 else "Please enter a correct value. "
                                      "Your name should only contain upper and lowercase letters.").ask()
    lastname = questionary.text("What is your last name? ",
                                validate=lambda text: True if len(text) > 0 and text.isalpha()
                                else "Please enter a correct value. "
                                     "Your name should only contain upper and lowercase letters.").ask()
    username = questionary.text("What is your username? ",
                                validate=lambda text: True if len(text) > 0 and text.isalnum()
                                else "Please enter a correct value. "
                                     "Your username can contain upper and lower case letters and numbers").ask()
    password = questionary.password("What is your password? ",
                                    validate=lambda text: True if len(text) >= 4 and text.isalnum()
                                    else "Your password must be at least four characters long and can "
                                         "contain upper and lower case letters and numbers.").ask()
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    new_user = User.UserClass(firstname, lastname, username, password)
    user = get_user(username)
    if user:
        print("\nThis username already exists. Try again!\n")
        register_user()

    else:
        new_user.store_in_db()
        print("\nRegistration successful!\n")


# FUNCTION TO RETRIEVE USERDATA FROM THE DB.
def get_user(username):
    """
    Retrieves all user data from the database for a specific user.

    Parameters
    ----------
    :param username: str
        Assigned to the function by register_user() or login().
    """

    from os.path import join, dirname, abspath
    db_path = join(dirname(abspath(__file__)), 'main_db.db')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    list_of_users = cur.fetchall()

    if len(list_of_users) > 0:
        firstname, lastname, username, password = list_of_users[0]
        user = User.UserClass(firstname, lastname, username, password)
        return user

    else:
        return None


# USER WILL BE ASKED FOR THEIR LOGIN DATA.
# IT IS CHECKED WHETHER THE USERNAME EXISTS.
# IT IS THEN CHECKED IF THE ENTERED PASSWORD IS CORRECT.
def login():
    """
    Function that regulates the login of a user.

    User is asked for their username and password and they are able to type in a text.
    It is checked whether the username exists. If yes, the entered password is checked.

    Returns
    -------
    :return:
        Returns the user to be allocated to the UserClass later on.
    """
    user_name = questionary.text("Enter your username: ").ask()
    user = get_user(user_name)
    if user:
        check_password(user.password)
        return user
    else:
        print("\nInvalid username.\n")
        login()


# ENTERED PASSWORD BY THE USER IS CHECKED WITH THE PASSWORD IN DB.
def check_password(password):
    """
    Entered passsword by the user is checked with the password in the database.

    :param password: str
        Assigned to the function by login().
        Password is hashed for data security reasons.
    """
    password_input = questionary.password("Enter your password: ").ask()
    password_input = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
    if password_input == password:
        print("\nLogin successful!\n")
    else:
        print("\nPassword incorrect. Try again!\n")
        check_password(password)
