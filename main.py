"""
This document regulates our user guidance. It represents the menu or the main navigation.

It imports the library 'questionary' as the Command Line Interface (CLI) that guides the user through the program
as well as checks the user input.
It also imports the initialisation.py doc which launches the core functionalities of the program.
"""
import questionary
import initialisation


# CREATES THE DATABASE.
initialisation.launch_database()


# PROGRAM STARTS AND INTRO MESSAGE INTRODUCES THE APP.
intro_message = "\n******************************\n" \
                "Welcome to Habit Tracker!\n" \
                "You can use this app to track your habits for a mindful life.\n" \
                "******************************\n"
print(intro_message)


# ASKS THE USER TO LOGIN OR REGISTER.
first_question = questionary.select(
    "Is this your first time here or have you been here before? ", choices=[
        "Register",
        "Login"
    ]).ask()

if first_question == "Login":
    user = initialisation.login()
    print("Welcome back!\n")

elif first_question == "Register":
    print("\nLooks like you're new here! Let's set up your profile.\n")
    initialisation.register_user()
    print("\nPlease log in:\n")
    user = initialisation.login()


# IF THE USER HAS NO HABITS SAVED, HE MUST CHOOSE FROM A PREDEFINED LIST OF HABITS.
user.choose_predefined_habit()


# FUNCTION THAT ASKS WHAT THE USER WANTS TO DO.
# THIS IS THE MAIN MENU OF OUR PROGRAM.
def menu():
    """
    This is the main menu of our program.

    It asks and prompts the user what they want to do and guides them through the programs functionalities.
    The user does not need to call any functions directly. They are always prompted if input is required.
    """
    second_question = questionary.select("What do you want to do? ",
                                         choices=[
                                             "Edit User Profile",
                                             "Create, Change or Mark a Habit as completed",
                                             "Activity Overview",
                                             "View Stats",
                                             "Exit Program"
                                         ]).ask()
    if second_question == "Edit User Profile":
        print("No problem. Let's edit your profile.\n")
        initialisation.get_user(user)
        user.update_profile()
        print("\nWhat do you want to do now?\n")
        menu()

    elif second_question == "Create, Change or Mark a Habit as completed":
        habit_question = questionary.select("Do you want to: ",
                                            choices=[
                                                "Create a new habit",
                                                "Delete habit",
                                                "Change an existing habit",
                                                "Mark a habit as completed"
                                            ]).ask()

        if habit_question == "Create a new habit":
            print("Let's create a habit.\n")
            new_habit = user.create_habit()
            user.store_habit_in_db(new_habit)
            print("\nWhat do you want to do now?\n")
            menu()

        elif habit_question == "Delete habit":
            user.delete_habit()
            print("\nWhat do you want to do now?\n")
            menu()

        elif habit_question == "Change an existing habit":
            print("Let's edit an existing habit!")
            user.update_habit()
            print("\nWhat do you want to do now?\n")
            menu()

        else:
            print("Let's mark a habit as completed.")
            user.is_completed()
            print("\nWhat do you want to do now?\n")
            menu()

    elif second_question == "Activity Overview":
        activity_question = questionary.select("Do you want to see...: ",
                                               choices=[
                                                   "all habits",
                                                   "all weekly habits",
                                                   "all daily habits"
                                               ]).ask()

        if activity_question == "all habits":
            print("\nYou currently have these habits saved:\n")
            user.show_all()
            print("\nWhat do you want to do now?\n")
            menu()

        elif activity_question == "all weekly habits":
            print("Your weekly habits are: \n")
            user.show_weekly_habits()
            print("\nWhat do you want to do now?\n")
            menu()

        else:
            print("Your daily habits are: \n")
            user.show_daily_habits()
            print("\nWhat do you want to do now?\n")
            menu()

    if second_question == "View Stats":
        stats_question = questionary.select("Do you want to see...: ",
                                            choices=[
                                                "your current streak overview",
                                                "your current streak per habit",
                                                "your longest streak per habit",
                                                "your longest streak overview (by periodicity)"
                                            ]).ask()
        if stats_question == "your current streak overview":
            user.current_streak_overview()
        elif stats_question == "your current streak per habit":
            user.current_streak_habit()
        elif stats_question == "your longest streak per habit":
            user.longest_streak_habit()
        else:
            user.longest_streak_overview()
        print("\nWhat do you want to do now?\n")
        menu()

    if second_question == "Exit Program":
        print(f"\nSee you soon, {user.firstname}!\n")


# EXECUTES THE FUNCTION DEFINED ABOVE AND STARTS THE USER GUIDANCE.
menu()
