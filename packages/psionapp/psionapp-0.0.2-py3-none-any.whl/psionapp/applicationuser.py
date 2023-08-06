import os

from .config import ConfigParser


class ApplicationUser(object):
    """
    A class that handles the creation and retrieval of user config records.

    Creates a config from an attributes dict.

    An attribute is keyed on the attribute name and is a tuple
    (config class, data type, initial value)
    """
    def __init__(self, *, app, user_id,  attributes):
        self.user_id = user_id
        super(ApplicationUser, self).__init__()
        self.attributes = attributes
        self.config = ConfigParser(self)
        self.config_file = os.sep.join([app.config_dir, f'{user_id}.ini'])

    def __str__(self):
        """A string summary of the User"""
        return f'ApplicationUser: {self.user_id}'

    def __repr__(self):
        """A string representation of the User"""
        repr_list = [f'id: {self.user_id}']
        for key, attribute in self.attributes.items():
            repr_list.append(f'{key}: ({attribute[0]}, {attribute[1]}, {str(attribute[2])})')
        repr = ',\n'.join(repr_list)
        return f'ApplicationUser: {repr}'

    def get_attributes(self, path):
        """Initialise the user from ini file or initial values."""
        self.config.get_attributes(path)
        self.config_file = path

    def save(self):
        """Save the config to file."""
        # path =  os.sep.join([app.config_dir, f'{self.user_id}.ini'])
        if self.config_file:
            self.config.save(self.config_file)


