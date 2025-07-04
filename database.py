import sqlite3

def conectar():
    conn = sqlite3.connect("data/gestor.db")
    return conn

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabla Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        organizacion TEXT,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
    ''')

    # Tabla Productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT,
        precio_compra REAL NOT NULL,
        precio_venta REAL NOT NULL,
        ganancia REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')

    # Tabla Ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        usuario_id INTEGER,
        fecha TEXT,
        cantidad INTEGER,
        ganancia REAL,
        FOREIGN KEY(producto_id) REFERENCES productos(id),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
