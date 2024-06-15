import os

SECRET_KEY = '46b74dc7229cda8e0de864283dd32b07ed850f59f97aa1e209fedabf28c81283'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2453_parinovadiana_exam:12345678@std-mysql.ist.mospolytech.ru/std_2453_parinovadiana_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')