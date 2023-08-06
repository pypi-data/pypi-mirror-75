from unittest import TestCase
import os
import username

username = username()


class TestUserIni(TestCase):
    """Appropriate creation of user.ini file."""
    def _remove_config_directory(self):
        """Remove the config directory."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        self.assertTrue(os.path.isdir(test_application.config_dir))
        test_application._remove_config_dir()
        self.assertFalse(os.path.isdir(test_application.config_dir))

    def test_create_user_ini(self):
        """After class TestApplicationDirsUser is created the user.ini file exists."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        ini_file = os.sep.join([test_application.config_dir, f'{username}.ini'])
        self.assertTrue(os.path.isfile(ini_file))

    def test_remove_user_ini(self):
        """Test that the TestApplicationDirsUser._remove_config_dir does delete the config directory."""
        self._remove_config_directory()

    def test_create_user_ini_after_delete(self):
        """ini_file is created after it is deleted and then instantiated."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        test_application._remove_config_dir()
        self.assertFalse(os.path.isdir(test_application.config_dir))
        test_application = TestApplicationDirsUser()
        ini_file = os.sep.join([test_application.config_dir, f'{username}.ini'])
        self.assertTrue(os.path.isfile(ini_file), f'{ini_file} is not a file.')

    def test_default_user_id_is_username(self):
        """The default user id is the user name."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        user = test_application.users[username]
        self.assertEqual(user.user_id, username, 'user.user_id')

    def test_ini_file_default_created_correctly(self):
        """The default ini file is in the correct format."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        user = test_application.users[username]
        self.assertEqual(user.string_data, 'abc', 'user.string_data')
        self.assertEqual(user.int_data, 2, 'user.int_data')
        self.assertTrue(user.bool_data is True, 'user.bool_data')
        self.assertEqual(user.float_data, 1.23456, 'user.float_data')

    def test_ini_file_updated_correctly(self):
        """The ini file updates correctly."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()

        # Set some values.
        user = test_application.users[username]
        user.string_data = 'xyz'
        user.int_data = 50
        user.bool_data = 'no'
        user.float_data = 0.000001
        user.save()

        # Re-open the application.
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        user = test_application.users[username]
        self.assertEqual(user.string_data, 'xyz', 'user.string_data')
        self.assertEqual(user.int_data, 50, 'user.int_data')
        self.assertTrue(user.bool_data is False, 'user.bool_data')
        self.assertEqual(user.float_data,  0.000001, 'user.float_data')

    def test_create_new_user(self):
        """A new user is created correctly."""
        from .classes_for_testing import TestApplicationDirsUser
        self._remove_config_directory()
        test_application = TestApplicationDirsUser()

        user = test_application.add_user('fred')
        self.assertEqual(user.user_id, 'fred', 'user.user_id')
        self.assertEqual(user.string_data, 'abc', 'user.string_data')
        self.assertEqual(user.int_data, 2, 'user.int_data')
        self.assertTrue(user.bool_data is True, 'user.bool_data')
        self.assertEqual(user.float_data, 1.23456, 'user.float_data')

    def test_switch_users(self):
        """Users are consistent."""
        from .classes_for_testing import TestApplicationDirsUser
        self._remove_config_directory()

        test_application = TestApplicationDirsUser()
        user = test_application.users[username]
        user.string_data = 'xyz'
        user.int_data = 50
        user.bool_data = 'no'
        user.float_data = 0.000001
        self.assertEqual(test_application.last_user_id, username, 'test_application.last_user')

        test_application.add_user('fred')
        self.assertEqual(test_application.last_user_id, username, 'test_application.last_user')
        test_application.switch_user('fred')
        self.assertEqual(test_application.last_user_id, 'fred', 'test_application.last_user')

        user = test_application.users[username]
        self.assertEqual(user.string_data, 'xyz', 'user.string_data')
        user = test_application.users['fred']
        self.assertEqual(user.string_data, 'abc', 'user.string_data')

    def test_add_user_invalid(self):
        """Users cannot be added if use_user_ini is False."""
        from .classes_for_testing import TestApplicationDirsNoConfigNoUser
        test_application = TestApplicationDirsNoConfigNoUser()
        self.assertRaises(ValueError, test_application.add_user, 'fred')

    def test_last_user_(self):
        """Last user updated correctly."""
        from .classes_for_testing import TestApplicationDirsUser
        self._remove_config_directory()
        test_application = TestApplicationDirsUser()
        self.assertEqual(test_application.last_user_id, username, 'test_application.last_user')

    def test_change_config_(self):
        """Error raised if config changed."""
        from .classes_for_testing import TestApplicationChangeConfig
        test_application = TestApplicationChangeConfig()
        user = test_application.users[username]
        user.save()
        self.assertEqual(user.integer_data, 2, 'user.integer_data')