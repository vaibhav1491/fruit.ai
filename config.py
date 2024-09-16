import os

class Config:
    # Use environment variable for sensitive data like DB credentials
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@host/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
