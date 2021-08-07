"""
This document contains the Habit Class.
It imports sqlite3.
"""
import sqlite3


# THE HABIT CLASS.
class HabitClass:
    """
    A class used to represent a habit.

    Attributes
    ----------

    habit_name: str
        the name of the habit
    owner: str
        the owner aka the user who the habit belongs to
    category: str
        the category the habit belongs to, which can be 'Fun', 'Health' or 'Mindfulness'
    periodicity: str
        the periodicity of the habit which can be 'weekly'  or 'daily'
    datetime_of_creation: datetime
        the date and time of when the habit was first created
    """

    # INIT METHOD.
    def __init__(self, habit_name, owner, category, periodicity, datetime_of_creation):
        """
        Parameters
        ----------
        :param habit_name: str
            the name of the habit
        :param owner: str
            the owner aka the user who the habit belongs to
        :param category: str
            the category the habit belongs to, which can be 'Fun', 'Health' or 'Mindfulness'
        :param periodicity: str
            the periodicity of the habit which can be 'weekly'  or 'daily'
        :param datetime_of_creation: datetime
            the date and time of when the habit was first created
        """
        self.habit_name = habit_name
        self.owner = owner
        self.category = category
        self.periodicity = periodicity
        self.datetime_of_creation = datetime_of_creation

        from os.path import join, dirname, abspath
        db_path = join(dirname(abspath(__file__)), 'main_db.db')

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()