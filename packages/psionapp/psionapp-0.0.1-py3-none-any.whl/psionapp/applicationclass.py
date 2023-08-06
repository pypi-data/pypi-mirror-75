"""A basic application class which applications can inherit."""
from .applicationbase import ApplicationBase


class ApplicationClass(ApplicationBase):
    """
    A class that forms the basis of an application.

    It uses ApplicationBase to retrieve any user configurations'
    """
    def __init__(self, *, id,
                 use_user_ini=False,
                 use_config_ini=False,
                 use_var_dir=False,
                 user_class=None,
                 attributes=None,
                 ):
        super(ApplicationClass, self).__init__(
            id,
            use_user_ini,
            use_config_ini,
            use_var_dir,
            user_class,
            attributes,
        )

        # General class variables
        self.id = id
        self.title = 'Application default Title'
        self.version = '0.0.0'

        # help
        self.help_url = ''

    def __str__(self):
        """A string summary of the application."""
        return f'Application - {self.title}, Version: {self.version}'

    def __repr__(self):
        """A string representation of the application."""
        repr_list = [
            f'id: {self.id}',
            f'title: {self.title}',
            f'uses user.ini: {self.use_user_ini}',
            f'uses control.ini: {self.use_config_ini}',
            f'uses var dir: {self.use_var_dir}',
        ]
        repr = ',\n'.join(repr_list)
        return f'ApplicationClass: {repr}'
