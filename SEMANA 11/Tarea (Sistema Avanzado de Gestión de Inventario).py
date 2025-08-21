#SEMANA 11 (SISTEMA AVANZADO DE GESTION DE INVENTARIO)
#NOMBRE: FLOR MUÑOZ

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import json
import os


@dataclass
class Producto:
    """Clase que representa un producto en inventario.

    Atributos:
        id: str - Identificador único del producto.
        nombre: str - Nombre del producto.
        cantidad: int - Cantidad disponible en inventario.
        precio: float - Precio unitario del producto.
    """

    id: str
    nombre: str
    cantidad: int
    precio: float

    def to_dict(self) -> Dict:
        """Convierte el objeto Producto a un diccionario serializable (para JSON)."""
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict) -> "Producto":
        """Crea un Producto desde un diccionario (deserialización)."""
        return Producto(id=d["id"], nombre=d["nombre"], cantidad=int(d["cantidad"]), precio=float(d["precio"]))


class Inventario:
    """Clase que gestiona la colección de productos.

    Internamente usa un diccionario para acceso rápido por ID: { id: Producto }
    """

    def __init__(self, storage_path: str = "inventory.json"):
        self.productos: Dict[str, Producto] = {}
        self.storage_path = storage_path

    # ---------- Operaciones CRUD ----------
    def añadir_producto(self, producto: Producto) -> bool:
        """Añade un nuevo producto. Devuelve True si se añadió, False si el ID ya existe."""
        if producto.id in self.productos:
            return False
        self.productos[producto.id] = producto
        return True

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto por su ID. Devuelve True si se eliminó, False si no existe."""
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False

    def actualizar_cantidad(self, producto_id: str, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto. Devuelve True si se actualizó, False si no existe."""
        p = self.productos.get(producto_id)
        if not p:
            return False
        p.cantidad = nueva_cantidad
        return True

    def actualizar_precio(self, producto_id: str, nuevo_precio: float) -> bool:
        """Actualiza el precio unitario de un producto."""
        p = self.productos.get(producto_id)
        if not p:
            return False
        p.precio = nuevo_precio
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos que contengan la cadena 'nombre' (búsqueda case-insensitive y parcial)."""
        nombre_lower = nombre.lower()
        return [p for p in self.productos.values() if nombre_lower in p.nombre.lower()]

    def mostrar_todos(self) -> List[Producto]:
        """Devuelve una lista de todos los productos ordenados por ID."""
        return [self.productos[k] for k in sorted(self.productos.keys())]

    # ---------- Persistencia en archivos (serialización JSON) ----------
    def guardar_en_archivo(self) -> None:
        """Serializa el inventario y lo guarda en self.storage_path (JSON)."""
        data = {pid: p.to_dict() for pid, p in self.productos.items()}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def cargar_desde_archivo(self) -> None:
        """Carga el inventario desde self.storage_path. Si el archivo no existe, no lanza error."""
        if not os.path.exists(self.storage_path):
            return
        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # data es un dict: { id: {id, nombre, cantidad, precio} }
        self.productos = {pid: Producto.from_dict(prod) for pid, prod in data.items()}


# ---------- Interfaz de consola / menú interactivo ----------

MENU = """
"SISTEMA AVANZADO DE GESTION DE INVENTARIO"
Seleccionar una opción:
1) Añadir nuevo producto
2) Eliminar producto por ID
3) Actualizar cantidad de producto
4) Actualizar precio de producto
5) Buscar productos por nombre
6) Mostrar todos los productos
7) Guardar inventario en archivo
8) Cargar inventario desde archivo
9) Salir
"""


def leer_no_vacio(prompt: str) -> str:
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("El valor no puede estar vacío. Intente de nuevo.")


def leer_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Por favor ingrese un número entero válido.")


def leer_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Por favor ingrese un número (puede tener decimales).")


def imprimir_producto(p: Producto) -> None:
    print(f"ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio:.2f}")


def main():
    inv = Inventario()
    # Cargar archivo al inicio si existe (comportamiento típico)
    inv.cargar_desde_archivo()
    print("Inventario cargado desde:", inv.storage_path)

    while True:
        print(MENU)
        opcion = input("Opción: ").strip()

        if opcion == "1":
            pid = leer_no_vacio("ID del producto: ")
            nombre = leer_no_vacio("Nombre: ")
            cantidad = leer_int("Cantidad (entera): ")
            precio = leer_float("Precio unitario: ")
            producto = Producto(id=pid, nombre=nombre, cantidad=cantidad, precio=precio)
            if inv.añadir_producto(producto):
                print("Producto añadido correctamente.")
            else:
                print("Error: ya existe un producto con ese ID.")

        elif opcion == "2":
            pid = leer_no_vacio("ID del producto a eliminar: ")
            if inv.eliminar_producto(pid):
                print("Producto eliminado.")
            else:
                print("No existe producto con ese ID.")

        elif opcion == "3":
            pid = leer_no_vacio("ID del producto a actualizar cantidad: ")
            if pid not in inv.productos:
                print("No existe producto con ese ID.")
            else:
                nueva = leer_int("Nueva cantidad (entera): ")
                inv.actualizar_cantidad(pid, nueva)
                print("Cantidad actualizada.")

        elif opcion == "4":
            pid = leer_no_vacio("ID del producto a actualizar precio: ")
            if pid not in inv.productos:
                print("No existe producto con ese ID.")
            else:
                nuevo = leer_float("Nuevo precio unitario: ")
                inv.actualizar_precio(pid, nuevo)
                print("Precio actualizado.")

        elif opcion == "5":
            nombre_busq = leer_no_vacio("Nombre o parte del nombre a buscar: ")
            encontrados = inv.buscar_por_nombre(nombre_busq)
            if not encontrados:
                print("No se encontraron productos.")
            else:
                print(f"Se encontraron {len(encontrados)} producto(s):")
                for p in encontrados:
                    imprimir_producto(p)

        elif opcion == "6":
            todos = inv.mostrar_todos()
            if not todos:
                print("El inventario está vacío.")
            else:
                print(f"Inventario ({len(todos)} productos):")
                for p in todos:
                    imprimir_producto(p)

        elif opcion == "7":
            inv.guardar_en_archivo()
            print(f"Inventario guardado en {inv.storage_path}.")

        elif opcion == "8":
            inv.cargar_desde_archivo()
            print(f"Inventario recargado desde {inv.storage_path}.")

        elif opcion == "9":
            # Guardar antes de salir (opcional: preguntar al usuario)
            guardar = input("¿Desea guardar el inventario antes de salir? (s/n): ").strip().lower()
            if guardar == "s":
                inv.guardar_en_archivo()
                print("Inventario guardado.")
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
