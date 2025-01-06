from flask_login import UserMixin
import random

class User(UserMixin):
    def __init__(self, password, username = ""):
        self.id = random.randint(100, 12000)
        self.username = username
        self.password = password


    def authenticate(self):
        from app.config import ADMIN_TOKEN
        if self.password == ADMIN_TOKEN:
            return True
        return False