from unittest import TestCase

import sys
import os
import initialisation
import User

# https://stackoverflow.com/a/11158224
sys.path.insert(1, os.path.join(sys.path[0], '..'))


class Test(TestCase):
    def test_get_user(self):
        test_user = initialisation.get_user("testuser1")
        non_existing_user = initialisation.get_user("non_existing_user")

        assert type(test_user) == User.UserClass
        assert non_existing_user is None