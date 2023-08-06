from unittest import TestCase
import os


class TestConfigDir(TestCase):
    """Test the appropriate creation of .config directory."""
    def _remove_config_directory(self):
        """Remove the config directory."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        self.assertTrue(os.path.isdir(test_application.config_dir))
        test_application._remove_config_dir()
        self.assertFalse(os.path.isdir(test_application.config_dir))

    def test_create_config_dir(self):
        """After class TestApplicationDirsUser is created the config directory exists."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        self.assertTrue(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')

    def test_remove_config_dir(self):
        """The TestApplicationDirsUser._remove_config_dir does delete the config directory."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        self.assertTrue(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')
        test_application._remove_config_dir()
        self.assertFalse(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')

    def test_create_config_dir_no_config(self):
        """If neither use_user_ini nor use_config_ini is True the config directory is not created."""
        from .classes_for_testing import TestApplicationDirsConfig
        from .classes_for_testing import TestApplicationDirsNoConfigNoUser
        test_application = TestApplicationDirsConfig()
        test_application._remove_config_dir()
        test_application = TestApplicationDirsNoConfigNoUser()
        self.assertFalse(os.path.isdir(test_application.config_dir), f'{test_application.config_dir} is a directory')

    def test_no_config_no_user_no_attributes(self):
        """With no config, user or attributes."""
        from .classes_for_testing import TestApplicationDirsNoConfigNoUser
        test_application = TestApplicationDirsNoConfigNoUser()
        self.assertFalse(test_application.config, 'test_no_config_no_user_no_attributes')

    def test_create_config_dir_config(self):
        """If use_config_ini is True the config directory is created."""
        from .classes_for_testing import TestApplicationDirsConfig
        test_application = TestApplicationDirsConfig()
        test_application._remove_config_dir()
        test_application = TestApplicationDirsConfig()
        self.assertTrue(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')

    def test_create_config_dir_user(self):
        """If neither use_user_ini is True the config directory is created."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        test_application._remove_config_dir()
        test_application = TestApplicationDirsUser()
        self.assertTrue(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')

    def test_create_config_file_created(self):
        """If neither use_user_ini is True the config directory is created."""
        from .classes_for_testing import TestApplicationDirsUser
        test_application = TestApplicationDirsUser()
        control_file_path = os.sep.join([test_application.config_dir, test_application.control_file_name])
        self.assertTrue(os.path.isfile(control_file_path), 'os.path.isfile(control_file_path)')

    def test_create_config_file_not_created(self):
        """If neither use_user_ini is True the config directory is created."""
        self._remove_config_directory()
        from .classes_for_testing import TestApplicationDirsNoConfigNoUser
        test_application = TestApplicationDirsNoConfigNoUser()
        control_file_path = os.sep.join([test_application.config_dir, test_application.control_file_name])
        self.assertFalse(os.path.isfile(control_file_path), 'os.path.isfile(control_file_path)')

    def test_create_config_dir_config_and_user(self):
        """If both use_user_ini and use_config_ini is True the config directory is created."""
        from .classes_for_testing import TestApplicationDirsConfigAndUser
        test_application = TestApplicationDirsConfigAndUser()
        test_application._remove_config_dir()
        test_application = TestApplicationDirsConfigAndUser()
        self.assertTrue(os.path.isdir(test_application.config_dir), 'os.path.isdir(test_application.config_dir)')


# class TestVarDir(TestCase):
#     """The appropriate creation of .var/app directory."""
    def test_create_var_dir(self):
        """Test that after class TestApplicationDirsVar is created the var/app directory exists."""
        from .classes_for_testing import TestApplicationDirsVar
        test_application = TestApplicationDirsVar()
        self.assertTrue(os.path.isdir(test_application.var_dir), 'os.path.isdir(test_application.config_dir)')

    def test_remove_var_dir(self):
        """The TestApplicationDirsUser._remove_var_dir does delete the var directory."""
        from .classes_for_testing import TestApplicationDirsVar
        test_application = TestApplicationDirsVar()
        self.assertTrue(os.path.isdir(test_application.var_dir), 'os.path.isdir(test_application.config_dir)')
        test_application._remove_var_dir()
        self.assertFalse(os.path.isdir(test_application.var_dir))

    def test_create_config_dir_no_var(self):
        """If use_var_dir is false the var dir is not created."""
        from .classes_for_testing import TestApplicationDirsVar
        test_application = TestApplicationDirsVar()
        test_application._remove_var_dir()
        from .classes_for_testing import TestApplicationDirsNoVar
        test_application = TestApplicationDirsNoVar()
        var_dir = test_application.var_dir
        self.assertFalse(os.path.isdir(var_dir), f'{var_dir} is a directory.')

    def test_create_var_dir_after_delete(self):
        """After class TestApplicationDirsUser is create the var directory exists."""
        from .classes_for_testing import TestApplicationDirsVar
        test_application = TestApplicationDirsVar()
        self.assertTrue(os.path.isdir(test_application.var_dir), 'os.path.isdir(test_application.config_dir)')
        test_application._remove_var_dir()
        test_application = TestApplicationDirsVar()
        self.assertTrue(os.path.isdir(test_application.var_dir), 'os.path.isdir(test_application.config_dir)')

