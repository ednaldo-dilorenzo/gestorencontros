from flask_login import UserMixin


class Usuario(UserMixin):
    def __init__(self, _id, username, password, name, matricula, papel, paroquia):
        self.id = _id
        self.username = username
        self.password = password
        self.name = name
        self.matricula = matricula
        self.papel = papel
        self.paroquia = paroquia
