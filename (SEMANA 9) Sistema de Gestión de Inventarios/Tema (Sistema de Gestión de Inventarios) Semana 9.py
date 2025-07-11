import os

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id_producto:<10} | {self.nombre:<20} | {self.cantidad:<8} | ${self.precio:<8.2f}"


# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar(self, producto):
        if any(p.id_producto == producto.id_producto for p in self.productos):
            print("❌ Ya existe un producto con ese ID.")
        else:
            self.productos.append(producto)
            print("✅ Producto agregado al inventario.")

    def eliminar(self, id_producto):
        for p in self.productos:
            if p.id_producto == id_producto:
                self.productos.remove(p)
                print("🗑️ Producto eliminado correctamente.")
                return
        print("⚠️ No se encontró un producto con ese ID.")

    def actualizar(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.id_producto == id_producto:
                if nueva_cantidad is not None:
                    p.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    p.precio = nuevo_precio
                print("✏️ Producto actualizado con éxito.")
                return
        print("⚠️ No se encontró un producto con ese ID.")

    def buscar(self, nombre):
        encontrados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]
        if encontrados:
            print("\n🔎 Resultados de búsqueda:")
            self.mostrar_tabla(encontrados)
        else:
            print("😕 No se encontraron productos con ese nombre.")

    def mostrar_todo(self):
        if self.productos:
            print("\n📦 Inventario completo:")
            self.mostrar_tabla(self.productos)
        else:
            print("📭 Inventario vacío.")

    def mostrar_tabla(self, lista):
        print("="*60)
        print(f"{'ID':<10} | {'Nombre':<20} | {'Cantidad':<8} | {'Precio':<8}")
        print("-"*60)
        for p in lista:
            print(p)
        print("="*60)

    def valor_total(self):
        total = sum(p.cantidad * p.precio for p in self.productos)
        print(f"\n💰 Valor total del inventario: ${total:.2f}")


# Interfaz de usuario
def menu():
    inventario = Inventario()

    while True:
        print("\n=== 📊 SISTEMA DE INVENTARIO CREATIVO ===")
        print("1️⃣ Añadir producto")
        print("2️⃣ Eliminar producto")
        print("3️⃣ Actualizar producto")
        print("4️⃣ Buscar producto por nombre")
        print("5️⃣ Mostrar inventario completo")
        print("6️⃣ Calcular valor total del inventario")
        print("7️⃣ Salir")

        opcion = input("\n👉 Selecciona una opción: ")

        if opcion == "1":
            id_producto = input("🔑 ID del producto: ")
            nombre = input("📛 Nombre: ")
            cantidad = int(input("📦 Cantidad: "))
            precio = float(input("💲 Precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar(producto)

        elif opcion == "2":
            id_producto = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese el ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (Enter si no cambia): ")
            precio = input("Nuevo precio (Enter si no cambia): ")
            inventario.actualizar(
                id_producto,
                nueva_cantidad=int(cantidad) if cantidad else None,
                nuevo_precio=float(precio) if precio else None
            )

        elif opcion == "4":
            nombre = input("Ingrese nombre o parte del nombre: ")
            inventario.buscar(nombre)

        elif opcion == "5":
            inventario.mostrar_todo()

        elif opcion == "6":
            inventario.valor_total()

        elif opcion == "7":
            print("👋 Gracias por usar el sistema, ¡hasta pronto!")
            break

        else:
            print("️Opción inválida, intente de nuevo.")


# Ejecutar el sistema
if __name__ == "__main__":
    menu()
