from firebase_admin      import App
from firebase_admin      import auth
from firebase_admin.auth import UserRecord

import firebase_admin

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Firebase(metaclass=Singleton):
    pass

class Setup(object):
    @staticmethod
    def create_instance():
        if not hasattr(Firebase, 'app'):
            Firebase.app = firebase_admin.initialize_app()