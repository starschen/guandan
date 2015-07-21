# Create dummy secrey key so we can use sessions
SECRET_KEY = '1234567890'

BASIC_AUTH_USERNAME = 'yourname'
BASIC_AUTH_PASSWORD = 'yourpass'
BASIC_AUTH_FORCE = True


"""
DB in remote host
"""
MONGODB_SETTINGS = {'db': "yourdb",
                    'username': 'username',
                    'password': 'pass',
                     'host': 'host',
                     'port': 27017
                     }

BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
