# services/citizens/project/config.py


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = 'my_precious'
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    pass


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
