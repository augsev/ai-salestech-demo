# auth.py
import bcrypt

from db.models import User
from db.database import Session


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


def add_user(username, password):
    session = Session()
    hashed_password = hash_password(password)
    new_user = User(username=username, passwd=hashed_password)
    session.add(new_user)
    session.commit()


def login_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(user.passwd, password):
        return True
    else:
        return False
