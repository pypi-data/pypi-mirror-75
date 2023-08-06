from unittest import TestCase
import username


class TestApplication(TestCase):
    def test_default_application_str(self):
        """The default str representation of the application."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        str_value = 'Application - Application default Title, Version: 0.0.0'
        self.assertEqual(str(test_application), str_value, 'default - str(test_application)')

    def test_modified_application_str(self):
        """The modified str representation of the application."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        test_application.title = 'Modified application'
        test_application.version = '1.2.3'
        str_value = 'Application - Modified application, Version: 1.2.3'
        self.assertEqual(str(test_application), str_value, 'modified - str(application)')

    def test_application_repr(self):
        """The repr representation of the application."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        repr_list = [
            'id: test_app',
            'title: Application default Title',
            'uses user.ini: False',
            'uses control.ini: True',
            'uses var dir: False',
        ]
        repr_base = ',\n'.join(repr_list)
        repr_str = f'ApplicationClass: {repr_base}'
        self.assertEqual(repr(test_application), repr_str, 'repr(application)')

    def test_application_user_str(self):
        """The str representation of the user."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        user = test_application.users[username()]
        str_value = f'ApplicationUser: {username()}'
        self.assertEqual(str(user), str_value, 'str(user)')

    def test_application_user_repr(self):
        """The repr representation of the user."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        user = test_application.users[username()]
        repr_list = [
            f'id: {username()}',
            'string_data: (general, string, abc)',
            'int_data: (general, int, 2)',
            'bool_data: (display, bool, True)',
            'float_data: (display, float, 1.23456)',
        ]
        repr_base = ',\n'.join(repr_list)
        repr_str = f'ApplicationUser:\n{repr_base}'
        self.assertEqual(repr(user), repr_str, 'repr(user)')

    def test_application_config(self):
        """The application level config."""
        from .classes_for_testing import TestApplicationDirsConfigAttributes
        test_application = TestApplicationDirsConfigAttributes()
        self.assertEqual(test_application.config_string_data, 'python', 'test_application_config')

    def test_application_str(self):
        """The str representation of the application."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        str_text = 'Application - Test class for use_user_ini=True, Version: 0.0.0'
        self.assertEqual(str(test_application), str_text, 'test_application_str')

    def test_application_repr(self):
        """The repr representation of the application."""
        from .classes_for_testing import TestApplicationDirsConfigAttributes
        test_application = TestApplicationDirsConfigAttributes()
        repr_list = [
            'id: test_app',
            'title: Class for testing application attributes',
            'uses user.ini: False',
            'uses control.ini: True',
            'uses var dir: False',
        ]
        repr_base = ',\n'.join(repr_list)
        repr_str = f'ApplicationClass:\n{repr_base}'
        self.assertEqual(repr(test_application), repr_str, 'repr(TestApplicationDirsConfigAttributes)')
