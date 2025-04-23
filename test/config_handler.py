from configparser import ConfigParser

def get_credentials():
    """Reads API credentials from config/config.properties."""
    config = ConfigParser()
    config.read('config/config.properties')
    username = config.get('testAPI', 'username')
    password = config.get('testAPI', 'password')
    return username, password

def get_api_url():
    """Reads API URL from config/config.properties."""
    config = ConfigParser()
    config.read('config/config.properties')
    return config.get('testAPI', 'baseUrl')
