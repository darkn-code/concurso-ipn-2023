from flask_login import UserMixin
from .firestore_service import get_user
class UserData:
    def __init__(self,username,password,name,fecha_nacimiento,correo_electronico):
        self.username = username
        self.password = password
        self.name = name
        self.fecha_nacimiento = fecha_nacimiento
        self.correo_electronico = correo_electronico

class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password
        self.name = user_data.name
        self.fecha_nacimiento = user_data.fecha_nacimiento
        self.correo_electronico = user_data.correo_electronico

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc['username'],
            password=user_doc['password'],
            name=user_doc['name'],
            fecha_nacimiento=user_doc['fecha_nacimiento'],
            correo_electronico=user_doc['correo_electronico']
        )

        return UserModel(user_data)
