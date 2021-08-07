from unittest import TestCase
from freezegun import freeze_time

import sys
import os
import Habit
import User
import initialisation

# https://stackoverflow.com/a/11158224
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class TestUserClass(TestCase):
    def test_get_habit(self):
        user = initialisation.get_user("testuser1")
        existing_habit = User.UserClass.get_habit(user, "Yoga")
        non_existing_habit = User.UserClass.get_habit(user, "non_existing_habit")
        assert type(existing_habit) == Habit.HabitClass
        assert non_existing_habit is None

    def test_show_all(self):
        user = initialisation.get_user("testuser1")
        all_habits = ["Yoga", "Walking", "Drawing", "Singing", "Meditation", "Journaling"]
        user_habits = User.UserClass.show_all(user)
        assert all_habits == user_habits

    def test_show_weekly_habits(self):
        user = initialisation.get_user("testuser1")
        weekly_habits = ["Yoga", "Drawing", "Meditation"]
        user_habits = User.UserClass.show_weekly_habits(user)
        assert weekly_habits == user_habits

    def test_show_daily_habits(self):
        user = initialisation.get_user("testuser1")
        daily_habits = ["Walking", "Singing", "Journaling"]
        user_habits = User.UserClass.show_daily_habits(user)
        assert daily_habits == user_habits

    def test_get_habit_progress(self):
        user = initialisation.get_user("testuser1")
        yoga_progress = [('2021-05-18 18:18:58.690152',), ('2021-05-25 18:00:31.108563',), ('2021-06-09 18:20:37.292187',),
                       ('2021-06-22 17:10:40.730695',), ('2021-06-25 18:30:54.475426',), ('2021-07-02 17:21:03.603940',),
                       ('2021-07-09 18:01:08.083291',), ('2021-07-11 16:21:21.358381',), ('2021-07-12 16:21:25.411913',),
                       ('2021-07-27 17:21:34.380509',), ('2021-08-06 14:27:40.303914',)]
        habit_progress = User.UserClass.get_habit_progress(user, "Yoga", "Weekly")
        assert yoga_progress == habit_progress

    # https://stackoverflow.com/a/17644388
    @freeze_time('2021-08-07')
    def test_compute_current_daily_streak(self):
        user = initialisation.get_user("testuser1")
        streak_walking = User.UserClass.compute_current_daily_streak(user, "Walking")
        print('streak_walking: {}'.format(streak_walking))
        assert streak_walking == 2

    def test_compute_current_weekly_streak(self):
        user = initialisation.get_user("testuser1")
        streak_yoga = User.UserClass.compute_current_weekly_streak(user, "Yoga")
        streak_drawing = User.UserClass.compute_current_weekly_streak(user, "Drawing")
        streak_non_existing_habit = User.UserClass.compute_current_weekly_streak(user, "non_existing_habit")
        assert streak_yoga == 2
        assert streak_drawing == 0
        assert streak_non_existing_habit == 0

    def test_compute_longest_daily_streak_habit(self):
        user = initialisation.get_user("testuser1")
        streak_walking = User.UserClass.compute_longest_daily_streak_habit(user, "Walking")
        streak_journaling = User.UserClass.compute_longest_daily_streak_habit(user, "Journaling")
        streak_non_existing_habit = User.UserClass.compute_longest_daily_streak_habit(user, "non_existing_habit")
        assert streak_walking == 4
        assert streak_journaling == 5
        assert streak_non_existing_habit == 0

    def test_compute_longest_weekly_streak_habit(self):
        user = initialisation.get_user("testuser1")
        streak_yoga = User.UserClass.compute_longest_weekly_streak_habit(user, "Yoga")
        streak_drawing = User.UserClass.compute_longest_weekly_streak_habit(user, "Drawing")
        streak_non_existing_habit = User.UserClass.compute_longest_weekly_streak_habit(user, "non_existing_habit")
        assert streak_yoga == 4
        assert streak_drawing == 5
        assert streak_non_existing_habit == 0