from models.database import SessionLocal
from models.user import User

class UserController:
    def __init__(self):
        self.session = SessionLocal()

    def add_user(self, username, password):
        if not username or not password:
            return False, "Usuario y contraseña son obligatorios."

        existing_user = self.session.query(User).filter_by(username=username).first()
        if existing_user:
            return False, "El usuario ya existe."

        new_user = User(username=username, password=password)
        self.session.add(new_user)
        self.session.commit()
        return True, "Usuario agregado con éxito."

    def get_users(self):
        return self.session.query(User).all()

    def authenticate_user(self, username, password):
        return self.session.query(User).filter_by(username=username, password=password).first()