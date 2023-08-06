from psionapp.applicationclass import ApplicationClass
from psionapp.applicationuser import ApplicationUser


class TestUser(ApplicationUser):
    def __init__(self, app, user_id=None):
        attributes = {
            'string_data': ('general', 'string', 'abc'),
            'int_data': ('general', 'int', 2),
            'bool_data': ('display', 'bool', True),
            'float_data': ('display', 'float', 1.23456),
        }
        super(TestUser, self).__init__(app=app, user_id=user_id, attributes=attributes)


class TestUserChange(ApplicationUser):
    def __init__(self, app, user_id=None):
        attributes = {
            'string_data': ('general', 'string', 'abc'),
            'integer_data': ('general', 'int', 2),
            'bool_data': ('display', 'bool', True),
            'float_data': ('display', 'float', 1.23456),
        }
        super(TestUserChange, self).__init__(app=app, user_id=user_id, attributes=attributes)


class TestApplicationDirsNoConfigNoUser(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsNoConfigNoUser, self).__init__(
            id='test_app',
            use_user_ini=False,
            use_config_ini=False,
            use_var_dir=False,
            user_class=False,
            **kwargs
        )


class TestApplicationDirsConfig(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsConfig, self).__init__(
            id='test_app',
            use_user_ini=False,
            use_config_ini=True,
            use_var_dir=False,
            user_class=TestUser,
            **kwargs
        )


class TestApplicationDirsConfigAttributes(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsConfigAttributes, self).__init__(
            id='test_app',
            use_user_ini=False,
            use_config_ini=True,
            use_var_dir=False,
            user_class=None,
            attributes = {
                'config_string_data': ('general', 'string', 'python'),
            },
            **kwargs
        )
        self.title = 'Class for testing application attributes'


class TestApplicationDirsUser(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsUser, self).__init__(
            id='test_app',
            use_user_ini=True,
            use_config_ini=False,
            use_var_dir=False,
            user_class=TestUser,
            **kwargs
        )
        self.title = 'Test class for use_user_ini=True'


class TestApplicationChangeConfig(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationChangeConfig, self).__init__(
            id='test_app',
            use_user_ini=True,
            use_config_ini=False,
            use_var_dir=False,
            user_class=TestUserChange,
            **kwargs
        )


class TestApplicationDirsConfigAndUser(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsConfigAndUser, self).__init__(
            id='test_app',
            use_user_ini=True,
            use_config_ini=True,
            use_var_dir=False,
            user_class=TestUser,
            **kwargs
        )


class TestApplicationDirsVar(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsVar, self).__init__(
            id='test_app',
            use_user_ini=False,
            use_config_ini=False,
            use_var_dir=True,
            user_class=TestUser,
            **kwargs
        )


class TestApplicationDirsNoVar(ApplicationClass):
    def __init__(self, *args, **kwargs):
        super(TestApplicationDirsNoVar, self).__init__(
            id='test_app',
            use_user_ini=False,
            use_config_ini=False,
            use_var_dir=False,
            user_class=TestUser,
            **kwargs
        )