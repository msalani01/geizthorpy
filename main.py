from crud import registrar_usuario, iniciar_sesion, agregar_producto, listar_productos, editar_producto, eliminar_producto, registrar_venta
from database import crear_tablas

def menu():
    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("👉 Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            organizacion = input("Organización: ")
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            registrar_usuario(nombre, organizacion, usuario, contrasena)
        elif opcion == "2":
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            usuario_id = iniciar_sesion(usuario, contrasena)
            if usuario_id:
                print("✅ Sesión iniciada.")
                menu_productos(usuario_id)  # 👉 Llama al menú de productos
            else:
                print("❌ Usuario o contraseña incorrectos.")
        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción no válida.")

def menu_productos(usuario_id):
    while True:
        print("\n📦 MENÚ PRODUCTOS")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Registrar venta")
        print("6. Volver")
        opcion = input("👉 Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            tipo = input("Tipo: ")
            precio_compra = float(input("Precio compra: "))
            precio_venta = float(input("Precio venta: "))
            stock = int(input("Stock: "))
            agregar_producto(nombre, tipo, precio_compra, precio_venta, stock)
        elif opcion == "2":
            listar_productos()
        elif opcion == "3":
            id_producto = int(input("ID del producto a editar: "))
            print("Deja en blanco los campos que no quieras cambiar.")
            nombre = input("Nuevo nombre: ") or None
            tipo = input("Nuevo tipo: ") or None
            precio_compra = input("Nuevo precio compra: ")
            precio_venta = input("Nuevo precio venta: ")
            stock = input("Nuevo stock: ")

            editar_producto(
                id_producto,
                nombre=nombre,
                tipo=tipo,
                precio_compra=float(precio_compra) if precio_compra else None,
                precio_venta=float(precio_venta) if precio_venta else None,
                stock=int(stock) if stock else None
            )
        elif opcion == "4":
            id_producto = int(input("ID del producto a eliminar: "))
            eliminar_producto(id_producto)
        elif opcion == "5":
            id_producto = int(input("ID del producto a vender: "))
            cantidad = int(input("Cantidad vendida: "))
            registrar_venta(id_producto, usuario_id, cantidad)
        elif opcion == "6":
            print("🔙 Volviendo al menú principal...")
            break
        else:
            print("⚠️ Opción no válida.")


def main():
    print("🛠️ Iniciando Gestor de Productos...")
    crear_tablas()
    menu()

if __name__ == "__main__":
    main()
