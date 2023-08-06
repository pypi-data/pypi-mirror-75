import os
from configparser import ConfigParser


class ConfigParser(ConfigParser):
    """A class that overrides ConfigParser to allow bespoke use of defaults and saves."""
    def __init__(self, client):
        super(ConfigParser, self).__init__()
        self.client = client
        self._get_default_config()
        self.get_attributes('')

    def get_attributes(self, path):
        """Initialise the client from ini file or initial values."""
        if os.path.isfile(path):
            self.read(path)
            for section in self:
                for att_name in self[section]:
                    if att_name in self.client.attributes:
                        data_type = self.client.attributes[att_name][1]
                        self.client.__dict__[att_name] = self._get_attribute_value(section, att_name, data_type)
                    # else:
                    #     raise KeyError(f'{att_name} is not in the config file!')
        else:
            self._get_default_config()

    def _get_default_config(self):
        """Retrieve the default values for the config."""
        for att_name, item in self.client.attributes.items():
            section = item[0]
            if section not in self:
                self[section] = {}
            default_value = item[2]
            self[section][att_name] = str(default_value)
            self.client.__dict__[att_name] = default_value

    def _get_attribute_value(self, section, att_name, data_type):
        """Return an attribute value of the correct type."""
        if data_type == 'int':
            value = self[section].getint(att_name)
        elif data_type == 'float':
            value = self[section].getfloat(att_name)
        elif data_type == 'bool':
            value = self[section].getboolean(att_name)
        else:
            value = self[section][att_name]
        return value

    def _update_config(self):
        """Update config with the current attribute values."""
        for att_name, item in self.client.attributes.items():
            section = item[0]
            self[section][att_name] = str(self.client.__dict__[att_name])

    def save(self, path):
        """Save the config to file."""
        self._update_config()
        with open(path, 'w') as config_file:
            self.write(config_file)
