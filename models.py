import hashlib

class Usuario:
    def __init__(self, id_usuario, nombre, organizacion, usuario, contrasena):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.organizacion = organizacion
        self.usuario = usuario
        self.contrasena = contrasena  # Contraseña encriptada

    @staticmethod
    def encriptar_contrasena(contrasena):
        return hashlib.sha256(contrasena.encode()).hexdigest()
