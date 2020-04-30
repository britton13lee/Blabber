Blabber
===================

CONFIGURATION:
---------------------

Structure a file called "mongo_settings.json" (pulled by SETTINGS_FILE environment variable) in the build directory as follows:
```json
{
    "host": "mongo",
    "port": "27017",
    "username": "mongodb",
    "password": "jslakjdf"
}
```

At a minimum, the file must specify the host and port. The username and password fields are optional.
By default, it will attempt to use "mongo" as the host on port 27017.
