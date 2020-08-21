from planner.pw import email_username, email_password, secret_key, sqlalchemy_database_uri
import os

class Config:
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = email_username
    MAIL_PASSWORD = email_password