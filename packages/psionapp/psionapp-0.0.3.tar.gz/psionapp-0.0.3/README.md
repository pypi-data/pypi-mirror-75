The **psionapp** package provides a basis for defining, saving, and retrieving application-level and user-level configuration variables (attributes).

The package exposes two classes: ApplicationClass and ApplicationUser.

###### ApplicationClass

An ApplicationClass object will define the application-level configuration (if any).

An ApplicationClass object will be identified by an *application id*. You can instantiate a class object with the following parameters:

* use_user_ini (bool). If True this will create a *<user name>.ini* file in the system appropriate *config* directory. Initially a file will be created for the current system user's user name. This will store user-level configuration values.

* use_config_ini (bool). If True this will create a *config.ini* file in the system appropriate *config* directory. This will store application-level configuration values.

* use_var_dir (bool). If True this will create an *application id* directory in the system appropriate *var data* directory.

* user_class (ApplicationUser). Used in conjunction with *use_user_ini*. The ApplicationUser class will define the config parameters.

* attributes (see [Attribute definition](attributes))

###### ApplicationUser

An ApplicationUser object will define the user-level configuration (if any).

An ApplicationUser class will be identified by a *user name*. It will define the attributes that will form that user's configuration values.

<span id="attributes"></span>
###### Attribute definition
Attibutes must be defined in the form:
```python
attributes = {
    'string_data': ('general', 'string', 'abc'),
    'int_data': ('general', 'int', 2),
    'bool_data': ('display', 'bool', True),
    'float_data': ('display', 'float', 1.23456),
}
```
where the *attributes* dict key is the attribute name, and the three tuple values are:
1. the section in the config file where the attribute will appear;
1. the data type of the attribute;
1. the default value of the attribute.
