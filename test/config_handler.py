from configparser import ConfigParser

def get_credentials():
    """Reads API credentials from config/config-test.properties."""
    config = ConfigParser()
    config.read('config/config-test.properties')
    username = config.get('testAPI', 'username')
    password = config.get('testAPI', 'password')
    return username, password

def get_api_url():
    """Reads API URL from config/config-test.properties."""
    config = ConfigParser()
    config.read('config/config-test.properties')
    return config.get('testAPI', 'baseUrl')
