import os

class DevelopmentConfig:
    PASS = os.getenv('pass')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{PASS}@localhost/advanced_e_commerce_db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True

