"""
This document contains our user class. The user class contains all the important functions of our programme.
Since our programme can create and manage several users, all functions always refer to the logged-in user.
This code part contains functions to manage the user profile, to create and manage user specific habits and
all functions around analysis.

It imports the libraries questionary, sqlite, datetime and hashlib.
It further imports the Habit.py document to be able to use the HabitClass.
"""
import questionary
import sqlite3
from datetime import datetime, timedelta
import Habit
import hashlib


# THE USER CLASS.
class UserClass:
    """
    A class used to represent a user.

    Attributes
    ----------
    firstname: str
        the firstname of the user
    lastname: str
        the lastname of the user
    username: str
        the username defined by the user
    password: str
        the password used by the user

    conn:
        Establishing a connection to the database

    Methods
    -------
    store_in_db()
        stores the user data into the database
    update_profile()
        function to be used to update user profile data
    store_habit_in_db(new_habit)
        stores a new habit into the database
    get_habit(habit_name)
        retrieves a habit from the database and gets all its information
    choose_predefined_habit()
        user can choose from a list of predefined habits if they have no habits stored in the db yet
    create_habit()
        lets the user create a new habit
    delete_habit()
        lets the user delete any habit from the db
    update_habit()
        lets the user update certain elements from their habit (periodicity, category)
    show_all()
        shows all habits of the user
    show_weekly_habits()
        shows all weekly habits of the user
    show_daily_habits()
        shows all daily habits of the user
    is_completed()
        herewith the user can mark a habit as done
    get_habit_progress(habit_name, periodicity)
        retrieves the progress of a certain habit with a certain periodicity from the database
    current_streak_overview()
        displays all current streaks of all habits of the user
    current_streak_habit()
        displays the current streak for a specific habit
    compute_current_daily_streak(habit_name)
        computes the current daily streak for a specific habit entered by the user
    compute_current_weekly_streak(habit_name)
        computes the current weekly streak for a specific habit entered by the user
    longest_streak_overview()
        displays the longest daily and the longest weekly streaks among all habits of the user
    longest_streak_habit()
        displays the longest streak for a specific habit
    compute_longest_daily_streak_habit(habit_name)
        computes the longest daily streak for a specific habit with the periodicity daily
    compute_longest_weekly_streak_habit(habit_name)
        computes the longest weekly streak for a specific habit with the periodicity weekly
    """

    # INIT METHOD.
    def __init__(self, firstname, lastname, username, password):
        """
        Parameters
        ----------
        :param firstname: the firstname of the user
        :param lastname: the lastname of the user
        :param username: the username defined by the user
        :param password: the password used by the user
        """
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password

        from os.path import join, dirname, abspath
        db_path = join(dirname(abspath(__file__)), 'main_db.db')

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    # This is followed by all functions that have to do with the user himself, such as editing the profile or similar.

    # STORES USER DATA INTO THE DATABASE.
    def store_in_db(self):
        """
        Stores the user data into the database.

        Function is used when first registering a user.

        """
        self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                         (self.firstname, self.lastname, self.username, self.password))
        self.conn.commit()

    # AN ALREADY REGISTERED USER CAN UPDATE THEIR PROFILE.
    def update_profile(self):
        """
        With this function an already registered user can update their profile.

        It is possible to choose between three elements to update: first name, last name and password.
        The user is asked to select one of the elements from a list.
        As soon as the user selected an element, they are asked to set a new first name / last name / password.
        The password must be at least four characters long and can contain upper and lower case letters and numbers.
        By pressing 'enter' the new entry is then saved in the database.
        The user is informed that his:her entry was updated.
        """
        element = questionary.select("What element do you want to change? ", choices=[
            "(1) first name",
            "(2) last name",
            "(3) password"
        ]).ask()
        if element == "(1) first name":
            new_firstname = questionary.text("What should your first name now be? ").ask()
            self.cur.execute(f"UPDATE users SET firstname = '{new_firstname}' WHERE username = '{self.username}';")
            self.cur.fetchall()
            self.conn.commit()
            print(f"\nYou successfully updated your name to '{new_firstname}'.\n")

        elif element == "(2) last name":
            new_lastname = questionary.text("What should your last name now be? ").ask()
            self.cur.execute(f"UPDATE users SET lastname = '{new_lastname}' WHERE username = '{self.username}';")
            self.cur.fetchall()
            self.conn.commit()
            print(f"\nYou successfully updated your name to '{new_lastname}'.\n")

        elif element == "(3) password":
            new_password = questionary.password("Enter a new password: ",
                                                validate=lambda text: True if len(text) >= 4 and text.isalnum()
                                                else "Your password must be at least four characters long and can "
                                                "contain upper and lower case letters and numbers.").ask()
            new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            self.cur.execute(f"UPDATE users SET password = '{new_password}' WHERE username = '{self.username}';")
            self.cur.fetchall()
            self.conn.commit()
            print(f"\nYou successfully updated your password.\n")


    # This is followed by all the functions that have to do with the basic creation of the Habits
    # and their storage and retrieval from the database.

    # THIS STORES HABIT DATA INTO THE DATABASE.
    def store_habit_in_db(self, new_habit):
        """
        Stores habit data into the database.

        Parameters
        ----------
        :param new_habit:
            Parameter is automatically assigned to the function. The function cannot be called directly,
            but is built in within other functions. There the habit attributes are defined and assigned
            to the parameter new_habit.
        """
        self.cur.execute("INSERT INTO habits VALUES(?, ?, ?, ?, ?)",
                         (new_habit.habit_name, new_habit.owner, new_habit.category, new_habit.periodicity,
                          new_habit.datetime_of_creation))
        self.conn.commit()

    # FUNCTION TO RETRIEVE HABIT FROM THE DB
    def get_habit(self, habit_name):
        """
        Retrieves the information of a habit from the database.

        Parameters
        ----------
        :param habit_name:
            The user is explicitly asked for the habit name so that the parameter is assigned.
            The function is not called directly but used elsewhere.

        Returns
        -------
        :return:
            Returns the habit.
            If no habit by the name (habit_name) is saved in the database, it returns None.
        """
        self.cur.execute(f"SELECT * FROM habits WHERE habit_name = '{habit_name}' AND owner = '{self.username}';")
        list_of_habits = self.cur.fetchall()
        if len(list_of_habits) > 0:
            habit_name, owner, category, periodicity, datetime_of_creation = list_of_habits[0]
            habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
            return habit
        else:
            return None

    # IF A USER HAS NO SAVED DATA IN THE DATABASE, THEY ARE ASKED TO CHOOSE FROM A LIST OF PREDEFINED HABITS.
    # THE USER CAN CHOOSE FROM THIS LIST AFTER INITIAL REGISTRATION.
    def choose_predefined_habit(self):
        """
        A user that has no saved habits can choose habits from a predefined list.

        Function first checks if a user has any saved habits. If they have, the function is skipped. If they have not
        they can choose from the list.
        The user is asked one by one if he/she wants to adopt the proposed habit. He/she answers by entering 'y' or 'Y'
        for yes and 'n' or 'N' for no. Depending on the answer, the habit is either stored in the database or passed.
        For this purpose the function store_habit_in_db(habit_name) is used.
        """
        self.cur.execute(f"SELECT * FROM habits WHERE owner = '{self.username}';")
        list_of_habits = self.cur.fetchall()

        if len(list_of_habits) > 0:
            pass

        else:
            print("It's your first time here - welcome! Let's choose your first habits:")
            first_habit = questionary.confirm("Yoga (weekly)").ask()
            second_habit = questionary.confirm("Walking (daily)").ask()
            third_habit = questionary.confirm("Drawing (weekly)").ask()
            fourth_habit = questionary.confirm("Singing (daily)").ask()
            fifth_habit = questionary.confirm("Meditation (weekly)").ask()
            sixth_habit = questionary.confirm("Journaling (daily)").ask()

            if first_habit:
                habit_name = "Yoga"
                owner = self.username
                category = "Health"
                periodicity = "Weekly"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

            if second_habit:
                habit_name = "Walking"
                owner = self.username
                category = "Health"
                periodicity = "Daily"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

            if third_habit:
                habit_name = "Drawing"
                owner = self.username
                category = "Fun"
                periodicity = "Weekly"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

            if fourth_habit:
                habit_name = "Singing"
                owner = self.username
                category = "Fun"
                periodicity = "Daily"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

            if fifth_habit:
                habit_name = "Meditation"
                owner = self.username
                category = "Mindfulness"
                periodicity = "Weekly"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

            if sixth_habit:
                habit_name = "Journaling"
                owner = self.username
                category = "Mindfulness"
                periodicity = "Daily"
                datetime_of_creation = datetime.now()
                new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
                self.store_habit_in_db(new_habit)
            else:
                pass

        self.conn.commit()

    # WITH THIS FUNCTION, A USER CAN CREATE A NEW HABIT
    def create_habit(self):
        """
        User can create a new habit.

        The user is asked a series of questions that allow him to create a new Habit.
        The user can create the habit name (the name can contain upper and lower case letters),
        he/she can choose from a list in which category the habit belongs (Health, Fun, Mindfulness),
        he/she can specify whether it is a "daily" or "weekly" habit.
        The assignment to the user = owner and the datetime_of_creation are created.
        After the input, get_habit(habit_name) is used to check if the habit already exists.

        Return
        ------
        :return:
            If the habit is not already in the database, the new habit is returned so it can be saved in the database
            with the function store_habit_in_db(new_habit) (this happens in the background, the user doesn't need to
            do anything)
        """
        habit_name = questionary.text("Type in the name of the habit: ",
                                      validate=lambda text: True if len(text) > 0 and text.isalpha()
                                      else "Please enter a correct value. "
                                           "Your habit name should only contain upper and lowercase letters.").ask()

        owner = self.username

        category = questionary.select("Your habit belongs to the category:",
                                      choices=[
                                          "Health",
                                          "Fun",
                                          "Mindfulness"
                                      ]).ask()

        periodicity = questionary.select("Is this a daily or weekly habit?",
                                         choices=[
                                             "Daily",
                                             "Weekly"
                                         ]).ask()

        datetime_of_creation = datetime.now()

        new_habit = Habit.HabitClass(habit_name, owner, category, periodicity, datetime_of_creation)
        existing_habit = self.get_habit(habit_name)
        if existing_habit:
            print("\nThis habit already exists. Try again!\n")
            self.create_habit()
        else:
            print("\nWell done! You created a new habit. \n")
            return new_habit

    # FUNCTION THAT REMOVES A HABIT OUT OF THE DB.
    def delete_habit(self):
        """
        Let's you remove aka delete a habit out of the database.

        User is asked to enter a habit name in a text field.
        The function checks with get_habit(habit_name) if the habit exists in the database.
        If it does not exist, it displays a print statement to the user.
        If it does exist, it deletes the habit out of the database and prints a success statement to the user.
        """
        habit_name = questionary.text("What habit do you want to delete? ",
                                      validate=lambda text: True if len(text) > 0 and text.isalpha()
                                      else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(habit_name)
        if existing_habit:
            self.cur.execute(f"DELETE FROM habits WHERE habit_name = '{habit_name}' AND owner = '{self.username}';")
            self.cur.fetchall()
            self.conn.commit()
            print(f"'{habit_name}' successfully deleted.")
        else:
            print("\nNo such habit in the database!\n")

    # HABIT ENTRY IS UPDATED.
    def update_habit(self):
        """
        Habit entry is updated.

        The CLI asks the user to enter the name of the habit they want to change. The user can enter a text.
        The function then checks if the habit exists in the database. If the user entered the name correctly, it
        gets the habit and asks the user to select which element they want to change.
        The user can select from a list of two (category or periodicity) and is then further prompted depending on the
        element they chose.
        After successful selection of the list items, the habit is adjusted accordingly in the database.
        """
        to_change = questionary.text("What habit do you want to change? ",
                                     validate=lambda text: True if len(text) > 0 and text.isalpha()
                                     else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(to_change)
        if existing_habit:
            element = questionary.select("What element do you want to change? ",
                                         choices=[
                                             "(1) category",
                                             "(2) periodicity",
                                         ]).ask()

            if element == "(1) category":
                new_category = questionary.select("Your habit belongs to the category:",
                                                  choices=[
                                                      "Health",
                                                      "Fun",
                                                      "Mindfulness"
                                                  ]).ask()
                self.cur.execute(f"UPDATE habits SET category = '{new_category}' WHERE habit_name = '{to_change}' "
                                 f"AND owner = '{self.username}';")
                self.cur.fetchall()
                print(f"\nYou successfully updated the category of your habit to '{new_category}'.\n")
                self.conn.commit()

            else:
                new_periodicity = questionary.select("Is this a daily or weekly habit?",
                                                     choices=[
                                                         "Daily",
                                                         "Weekly"
                                                     ]).ask()
                self.cur.execute(
                    f"UPDATE habits SET periodicity = '{new_periodicity}' WHERE habit_name = '{to_change}' "
                    f"AND owner = '{self.username}';")
                self.cur.execute(
                    f"UPDATE progress SET periodicity = '{new_periodicity}' WHERE habit_name = '{to_change}' "
                    f"AND owner = '{self.username}';")
                self.cur.fetchall()
                print(f"\nYou successfully updated the periodicity of your habit to '{new_periodicity}'.\n")
                self.conn.commit()

        else:
            print("This habit is not in the database.")

    # The following are the functions that give an overview of all the habits.

    # QUERIES THE DB AND RETURNS A LIST OF ALL HABITS OF THE USER.
    def show_all(self):
        """
        Queries the database and prints a list of all habits of the currently logged in user.

        Returns
        -------
        :return: list
            returns a list of all habits
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # QUERIES THE DB AND RETURNS A LIST OF WEEKLY HABITS OF THE USER.
    def show_weekly_habits(self):
        """
        Queries the database and returns a list of the weekly habits of the currently logged in user.

        Returns
        -------
        :return: list
            returns a list of weekly habits
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE periodicity = 'Weekly' AND owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # QUERIES THE DB AND RETURNS A LIST OF ALL DAILY HABITS OF THE USER.
    def show_daily_habits(self):
        """
        Queries the database and returns a list of the daily habits of the currently logged in user.

        Returns
        -------
        :return: list
            returns a list of all daily habits
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE periodicity = 'Daily' AND owner = '{self.username}';")
        items = self.cur.fetchall()
        habits = []
        for item in items:
            habits.append(item[0])
        print(habits)
        return habits

    # The functions that deal with the analysis of the habits follow.

    # HABIT IS MARKED AS DONE. THE ENTRY IS SAVED IN THE DB.
    def is_completed(self):
        """
        A user can mark a habit is done.

        The program prompts the user to enter the name of the habit they want to mark as completed.
        They are only able to enter upper and lowercase letters.
        If the habit exists in the database, the program sets the date and time of completion and saved the progress
        in the progress table of the database.
        The user is informed via print statement if they were successful with the completion progress.
        """
        to_complete = questionary.text("What habit do you want to mark as completed? ",
                                       validate=lambda text: True if len(text) > 0 and text.isalpha()
                                       else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(to_complete)

        if existing_habit:
            datetime_of_completion = datetime.now()
            self.cur.execute("INSERT INTO progress VALUES(?, ?, ?, ?)",
                             (existing_habit.habit_name, existing_habit.periodicity, self.username,
                              datetime_of_completion))
            self.conn.commit()
            print("Yippie! You completed your habit. Well done!")

        else:
            print("This habit does not exist.")

    # GETS ALL SAVED PROGRESS DATA OF A USER.
    def get_habit_progress(self, habit_name, periodicity):
        """
        Gets the date and time of completion of a specific habit from the progress table of the database.

        Parameters
        ----------
        Both parameters are assigned within the functions compute_current_daily_streak, compute_current_weekly_streak,
        compute_longest_daily_streak or compute_longest_weekly_streak.

        :param habit_name:
            int
        :param periodicity:
            int --> 'Daily' or 'Weekly'

        Returns
        -------
        :return:
            user_progress --> if there is any saved progress in the database
            None --> if there is no progress saved
        """
        self.cur.execute(f"SELECT datetime_of_completion FROM progress "
                         f"WHERE owner = '{self.username}' AND habit_name = '{habit_name}' "
                         f"AND periodicity = '{periodicity}';")
        user_progress = self.cur.fetchall()

        if len(user_progress) > 0:
            return user_progress

        else:
            return None

    # Everything that has to do with the current streak of the habits.

    # SHOWS THE USER A CURRENT STREAK OVERVIEW OF ALL THEIR HABITS SORTED BY PERIODICITY
    def current_streak_overview(self):
        """
        Shows the user a current streak overview of all their habits sorted by periodicity.

        First selects all daily habits from the database with the owner == user and prints them to the user.
        Then selects all weekly habits from the database with the owner == user and prints them.
        """
        self.cur.execute(f"SELECT habit_name FROM habits WHERE owner = '{self.username}' AND periodicity = 'Daily';")
        items = self.cur.fetchall()
        for item in items:
            habit_name = item[0]
            daily_streak = self.compute_current_daily_streak(habit_name)
            print(f"The current streak of {habit_name} is: ", daily_streak, " day(s)")

        self.cur.execute(f"SELECT habit_name FROM habits WHERE owner = '{self.username}' AND periodicity = 'Weekly';")
        items = self.cur.fetchall()
        for item in items:
            habit_name = item[0]
            weekly_streak = self.compute_current_weekly_streak(habit_name)
            print(f"The current streak of {habit_name} is: ", weekly_streak, " week(s)")

    # RETURNS THE CURRENT STREAK OF A HABIT.
    # AUTOMATICALLY FILTERS IF THE HABIT IS A DAILY OR WEEKLY HABIT AND OUTPUTS THE DATA ACCORDINGLY.
    def current_streak_habit(self):
        """
        Returns the current streak of a specific habit from the logged in user.

        User is asked to enter a habit name.
        If the habit exists, the function gets its periodicity.
        If the periodicity is 'Daily' it calls the function compute_current_daily_streak, otherwise it calls the
        function compute_current_weekly_streak
        """
        habit_name = questionary.text("For which habit do you want to see the current streak? ",
                                      validate=lambda text: True if len(text) > 0 and text.isalpha()
                                      else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(habit_name)
        periodicity = existing_habit.periodicity

        if existing_habit:
            if periodicity == "Daily":
                streak = self.compute_current_daily_streak(habit_name)
                if streak is not None:
                    print(f"The current streak of {habit_name} is: ", streak, " day(s)")
                else:
                    print("This habit does not exist.")

            else:
                streak = self.compute_current_weekly_streak(habit_name)
                if streak is not None:
                    print(f"The current streak of {habit_name} is: ", streak, " week(s)")
                else:
                    print("This habit does not exist.")
        else:
            print("This habit does not exist.")

    # COMPUTES THE CURRENT STREAK OF A HABIT WITH THE PERIODICITY DAILY
    def compute_current_daily_streak(self, habit_name):
        """
        Computes the current streak of a habit with the periodicity daily.

        Function cannot be called directly by the user but is used within other functions.

        Parameters
        ----------
        :param habit_name: str
            Is assigned by the functions current_streak_habit and current_streak_overview.

        Returns
        -------
        :return: int
            Returns a number as the streak count (zero to infinite)
            Gives it to the functions current_streak_habit and current_streak_overview to be displayed to the user.
        """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity="Daily")
        if habit_progress_total is None:
            return 0
        ref = datetime.now() - timedelta(days=1)
        habits = []
        for habit in reversed(habit_progress_total):
            habit = datetime.strptime(habit[0], '%Y-%m-%d %H:%M:%S.%f')
            habits.append(habit)
        streak = 1 if datetime.now().date() == habits[0].date() else 0

        for habit in habits[streak:]:
            if habit.date() == ref.date():
                streak += 1
                ref -= timedelta(days=1)
            else:
                break

        return streak

    # COMPUTES THE CURRENT STREAK OF A HABIT WITH THE PERIODICITY WEEKLY
    def compute_current_weekly_streak(self, habit_name):
        """
        Computes the current streak of a habit with the periodicity weekly.

        Function cannot be called directly by the user but is used within other functions.

        Parameters
        ----------
        :param habit_name: str
            Is assigned by the functions current_streak_habit and current_streak_overview.

        Returns
        -------
        :return: int
            Returns a number as the streak count (zero to infinite)
            Gives it to the functions current_streak_habit and current_streak_overview to be displayed to the user.
        """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity="Weekly")
        if habit_progress_total is None:
            return 0

        # saves all habits in a list
        habits = []
        for habit in reversed(habit_progress_total):
            x = datetime.strptime(habit[0], '%Y-%m-%d %H:%M:%S.%f')
            habits.append(x)

        # finds out which calendar week the stored data corresponds to
        calendar_weeks = []
        for n in range(0, len(habits)):
            weeks = habits[n].isocalendar()[1]
            calendar_weeks.append(weeks)

        # deletes all duplicate / same values, so that the calendar week is stored only once
        adj_calendar_weeks = []
        x = []
        for e in calendar_weeks:
            if e not in x:
                adj_calendar_weeks.append(e)
                x.append(e)

        now = datetime.now()
        now_week = now.isocalendar()[1]

        # computes the streak
        streak = []
        if len(adj_calendar_weeks) == 1:
            if adj_calendar_weeks[0] == now_week:
                streak.append(1)
                list_sum = sum(streak)
                return list_sum

        elif len(adj_calendar_weeks) >= 2 and adj_calendar_weeks[0] == now_week:
            streak.append(1)
            for n in range(0, len(adj_calendar_weeks)-1):
                x = adj_calendar_weeks[n] - adj_calendar_weeks[n + 1]
                if x == 1:
                    streak.append(1)
                else:
                    break
            list_sum = sum(streak)
            return list_sum
        else:
            return 0

    # Everything that has to do with the longest streak of the habits.

    # SHOWS THE USER THEIR LONGEST STREAK OF ALL THEIR HABITS SORTED BY PERIODICITY
    def longest_streak_overview(self):
        """
        Shows the user their longest streak of all their habits sorted by periodicity.

        First selects all daily habits from the database with the owner == user,
        then computes the longest streak from all habits and then prints the longest one to the user.

        Then selects all weekly habits from the database with the owner == user,
        then computes the longest streak from all habits and then prints the longest one to the user.
        """
        # daily habits
        self.cur.execute(f"SELECT habit_name FROM habits WHERE owner = '{self.username}' AND periodicity = 'Daily';")
        all_daily_habits = self.cur.fetchall()
        daily_habits = []
        for habit in all_daily_habits:
            daily_habits.append(habit)

        streaks = []
        for habit in daily_habits:
            longest_daily_habit_streak = self.compute_longest_daily_streak_habit(habit[0])
            streaks.append((habit[0], longest_daily_habit_streak))

        max_value = max(streaks, key=lambda e: e[1])
        print(f"Your longest daily streak among all your daily habits is {max_value[1]} day(s). "
              f"The habit '{max_value[0]}' is your strongest!")

        # weekly habits
        self.cur.execute(f"SELECT habit_name FROM habits WHERE owner = '{self.username}' AND periodicity = 'Weekly';")
        all_weekly_habits = self.cur.fetchall()
        weekly_habits = []
        for habit in all_weekly_habits:
            weekly_habits.append(habit)

        streaks = []
        for habit in weekly_habits:
            longest_weekly_habit_streak = self.compute_longest_weekly_streak_habit(habit[0])
            streaks.append((habit[0], longest_weekly_habit_streak))

        max_value = max(streaks, key=lambda e: e[1])
        print(f"Your longest weekly streak among all your weekly habits is {max_value[1]} weeks(s). "
              f"You're doing great with habit '{max_value[0]}'!")

    # ASKS THE USER FOR WHICH HABIT THEY WANT TO SEE THE LONGEST STREAK.
    # THEN SHOWS THE LONGEST STREAK FOR THE CHOSEN HABIT.
    # AUTOMATICALLY FILTERS IF THE HABIT IS DAILY OR WEEKLY.
    def longest_streak_habit(self):
        """
        Shows the longest streak for a chosen habit.

        Asks the user for which habit they want to see the longest streak.
        Automatically filters if the habit is daily or weekly.
        Uses the functions get_habit(), compute_longest_daily_streak_habit(), compute_longest_weekly_streak_habit().
        """
        habit_name = questionary.text("For which habit do you want to see your longest streak? ",
                                      validate=lambda text: True if len(text) > 0 and text.isalpha()
                                      else "Please enter a correct value.").ask()
        existing_habit = self.get_habit(habit_name)
        periodicity = existing_habit.periodicity

        if existing_habit:
            if periodicity == "Daily":
                streak = self.compute_longest_daily_streak_habit(habit_name)
                if streak is not None:
                    print(f"The longest streak of {habit_name} is: ", streak, " day(s)")
            else:
                streak = self.compute_longest_weekly_streak_habit(habit_name)
                if streak is not None:
                    print(f"The longest streak of {habit_name} is: ", streak, " week(s)")

        else:
            print("This habit does not exist.")

    # COMPUTES THE LONGEST STREAK OF A HABIT WITH THE PERIODICITY DAILY
    def compute_longest_daily_streak_habit(self, habit_name):
        """
        Computes the longest streak of a habit with the periodicity daily.

        Pulls all progress data from the database, stores and cleans the data in a list. Subtracts the values from each
        other. The differences are saved in a new list. The streak is calculated if the number is a 1,
        otherwise the loop breaks, then the maximum streak count is determined.

        Parameters
        ----------
        :param habit_name: str
            Is assigned through the functions longest_streak_habit() and longest_streak_overview()

        Returns
        -------
        :return: int
             Returns a number from 0 to infinite (max_value) as the longest streak count.
        """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity="Daily")
        if habit_progress_total is None:
            return 0

        habits = []
        for habit in reversed(habit_progress_total):
            habit = datetime.strptime(habit[0], '%Y-%m-%d %H:%M:%S.%f')
            habits.append(habit)

        # calculates the difference between the values
        diff = []
        streak = 1 if datetime.now().date() == habits[0].date() else 0
        diff.append(streak)

        for n in range(0, len(habits)-1):
            difference = habits[n].date() - habits[n+1].date()
            diff.append(difference.days)

        # cleans up the differences in the list for easier reuse
        adj_diff = [99]
        for n in diff:
            if n == 1:
                adj_diff.append(1)
            elif n == 0 and adj_diff[-1] != 0:
                adj_diff.append(0)
            elif n != 0:
                adj_diff.append(99)

        temp_diff = []
        for i in range(1, len(adj_diff)-1):
            if adj_diff[i] == 99 and adj_diff[i+1] == 1:
                temp_diff.append(99)
                temp_diff.append(1)
            else:
                temp_diff.append(adj_diff[i])

        final_diff = temp_diff + adj_diff[-1:]

        for i in range(len(final_diff)):
            if final_diff[i] == 0:
                final_diff[i] = 1

        # calculates the streak
        # stores the values in the cache until a 99 appears
        # then the loop breaks, the values are summed and the max. value is output
        streak_count = []
        cache = []
        for n in final_diff:
            if n == 1:
                cache.append(1)
            else:
                list_sum = sum(cache)
                streak_count.append(list_sum)
                cache.clear()
                continue
        list_sum = sum(cache)
        streak_count.append(list_sum)

        max_value = max(streak_count)
        return max_value

    # COMPUTES THE LONGEST STREAK OF A HABIT WITH THE PERIODICITY WEEKLY
    def compute_longest_weekly_streak_habit(self, habit_name):
        """
        Computes the longest streak of a habit with the periodicity weekly.

        Pulls all progress data from the database, stores and cleans the data in a list. Subtracts the values from each
        other. The differences are saved in a new list.
        The streak is calculated and the maximum streak count is returned.

        Parameters
        ----------
        :param habit_name: str
            Is assigned through the functions longest_streak_habit() and longest_streak_overview()

        Returns
        -------
        :return: int
             Returns a number from 0 to infinite (max_value) as the longest streak count.
        """
        habit_progress_total = self.get_habit_progress(habit_name, periodicity="Weekly")
        if habit_progress_total is None:
            return 0

        habits = []
        for habit in reversed(habit_progress_total):
            habit = datetime.strptime(habit[0], '%Y-%m-%d %H:%M:%S.%f')
            habits.append(habit)

        # finds out which calendar week the stored data corresponds to
        calendar_weeks = []
        for n in range(0, len(habits)):
            weeks = habits[n].isocalendar()[1]
            calendar_weeks.append(weeks)

        # deletes all duplicate / same values, so that the calendar week is stored only once
        adj_calendar_weeks = []
        x = []
        for e in calendar_weeks:
            if e not in x:
                adj_calendar_weeks.append(e)
                x.append(e)

        # computes the difference between the calendar weeks
        diff = [1]
        for n in range(0, len(adj_calendar_weeks)-1):
            x = adj_calendar_weeks[n] - adj_calendar_weeks[n+1]
            diff.append(x)

        if len(adj_calendar_weeks) >= 2:
            if adj_calendar_weeks[-1] != adj_calendar_weeks[-2]:
                diff.append(1)

            adj_diff = [1]
            for i in range(1, len(diff)-1):
                if diff[i] > 1 and diff[i+1] == 1:
                    adj_diff.append(99)
                    adj_diff.append(1)
                else:
                    adj_diff.append(diff[i])

            # calculates the streak
            # stores the values in the cache until a 99 appears
            # then the loop breaks, the values are summed and the max. value is output
            streak_count = []
            cache = []
            for n in adj_diff:
                if n == 1:
                    cache.append(1)
                else:
                    list_sum = sum(cache)
                    streak_count.append(list_sum)
                    cache.clear()
                    continue
            list_sum = sum(cache)
            streak_count.append(list_sum)

            max_value = max(streak_count)
            return max_value
        else:
            return 1
