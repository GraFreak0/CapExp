from configparser import ConfigParser

def get_credentials():
    """Reads API credentials from config/config.properties."""
    config = ConfigParser()
    config.read('config/config.properties')
    username = config.get('API', 'username')
    password = config.get('API', 'password')
    return username, password

def get_api_url():
    """Reads API URL from config/config.properties."""
    config = ConfigParser()
    config.read('config/config.properties')
    return config.get('API', 'baseUrl')
