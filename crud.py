import sqlite3
from datetime import datetime
from database import conectar
from models import Usuario

# Registrar usuario
def registrar_usuario(nombre, organizacion, usuario, contrasena):
    conn = conectar()
    cursor = conn.cursor()

    contrasena_hash = Usuario.encriptar_contrasena(contrasena)

    try:
        cursor.execute("INSERT INTO usuarios (nombre, organizacion, usuario, contrasena) VALUES (?, ?, ?, ?)",
                       (nombre, organizacion, usuario, contrasena_hash))
        conn.commit()
        print("✅ Usuario registrado correctamente.")
    except Exception as e:
        print("❌ Error al registrar usuario:", e)
    finally:
        conn.close()

# Iniciar sesión
def iniciar_sesion(usuario, contrasena):
    conn = conectar()
    cursor = conn.cursor()

    contrasena_hash = Usuario.encriptar_contrasena(contrasena)
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?", (usuario, contrasena_hash))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        print(f"🎉 Bienvenido {resultado[1]} de {resultado[2]}")
        return resultado[0]  # 👈 Devuelve el ID del usuario
    else:
        print("❌ Usuario o contraseña incorrectos.")
        return None


# AGREGAR PRODUCTO
def agregar_producto(nombre, tipo, precio_compra, precio_venta, stock):
    conn = conectar()
    cursor = conn.cursor()
    try:
        ganancia = precio_venta - precio_compra
        cursor.execute("""
            INSERT INTO productos (nombre, tipo, precio_compra, precio_venta, ganancia, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, precio_compra, precio_venta, ganancia, stock))
        conn.commit()
        print("✅ Producto agregado correctamente.")
    except Exception as e:
        print("❌ Error al agregar producto:", e)
    finally:
        conn.close()

# LISTAR PRODUCTOS
def listar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    if productos:
        print("\n📦 Lista de Productos:")
        for p in productos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Tipo: {p[2]} | Compra: {p[3]} | Venta: {p[4]} | Ganancia: {p[5]} | Stock: {p[6]}")
    else:
        print("⚠️ No hay productos registrados.")

# EDITAR PRODUCTO
def editar_producto(id_producto, nombre=None, tipo=None, precio_compra=None, precio_venta=None, stock=None):
    conn = conectar()
    cursor = conn.cursor()

    # Obtener producto actual
    cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        print("❌ Producto no encontrado.")
        conn.close()
        return

    # Actualizar campos
    nuevo_nombre = nombre if nombre else producto[1]
    nuevo_tipo = tipo if tipo else producto[2]
    nuevo_precio_compra = precio_compra if precio_compra else producto[3]
    nuevo_precio_venta = precio_venta if precio_venta else producto[4]
    nueva_ganancia = nuevo_precio_venta - nuevo_precio_compra
    nuevo_stock = stock if stock is not None else producto[6]

    try:
        cursor.execute("""
            UPDATE productos
            SET nombre=?, tipo=?, precio_compra=?, precio_venta=?, ganancia=?, stock=?
            WHERE id=?
        """, (nuevo_nombre, nuevo_tipo, nuevo_precio_compra, nuevo_precio_venta, nueva_ganancia, nuevo_stock, id_producto))
        conn.commit()
        print("✅ Producto actualizado correctamente.")
    except Exception as e:
        print("❌ Error al actualizar producto:", e)
    finally:
        conn.close()

# ELIMINAR PRODUCTO
def eliminar_producto(id_producto):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
        conn.commit()
        print("🗑️ Producto eliminado correctamente.")
    except Exception as e:
        print("❌ Error al eliminar producto:", e)
    finally:
        conn.close()

def registrar_venta(producto_id, usuario_id, cantidad):
    conn = conectar()
    cursor = conn.cursor()

    # Obtener datos del producto
    cursor.execute("SELECT stock, precio_compra, precio_venta FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()

    if producto is None:
        print("❌ Producto no encontrado.")
        conn.close()
        return

    stock_actual, precio_compra, precio_venta = producto

    if stock_actual < cantidad:
        print(f"⚠️ Stock insuficiente. Stock disponible: {stock_actual}")
        conn.close()
        return

    # Calcular ganancia
    ganancia_unitaria = precio_venta - precio_compra
    ganancia_total = ganancia_unitaria * cantidad

    # Actualizar stock y sumar ganancia
    nuevo_stock = stock_actual - cantidad
    cursor.execute("""
        UPDATE productos
        SET stock = ?, ganancia = ganancia + ?
        WHERE id = ?
    """, (nuevo_stock, ganancia_total, producto_id))

    # Registrar la venta en la tabla ventas
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO ventas (producto_id, usuario_id, fecha, cantidad, ganancia)
        VALUES (?, ?, ?, ?, ?)
    """, (producto_id, usuario_id, fecha_actual, cantidad, ganancia_total))

    conn.commit()
    conn.close()

    print(f"✅ Venta registrada correctamente. Stock restante: {nuevo_stock}")