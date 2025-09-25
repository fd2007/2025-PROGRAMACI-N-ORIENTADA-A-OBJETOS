# ------------------------------
# archivo: producto.py
# ------------------------------
"""
Clase Producto
Atributos: id, nombre, cantidad, precio
Métodos: getters, setters, conversiones a dict/string
"""
from csv import DictWriter


class Producto:
    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        self.id = str(id_producto)
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": str(self.cantidad),
            "precio": str(self.precio),
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], int(d["cantidad"]), float(d["precio"]))

    def __str__(self):
        return f"{self.id} - {self.nombre} (x{self.cantidad}) ${self.precio:.2f}"


# ------------------------------
# archivo: inventario.py
# ------------------------------
"""
Clase Inventario
"""
import csv
from typing import List, Optional, Any, TextIO


class Inventario:
    def __init__(self):
        # Usamos lista de objetos Producto
        self.productos: List[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        # si ya existe id, reemplaza o suma: aquí elegimos reemplazar
        existing = self.obtener_producto(producto.id)
        if existing:
            raise ValueError(f"Producto con ID {producto.id} ya existe.")
        self.productos.append(producto)

    def eliminar_producto(self, id_producto: str) -> bool:
        p = self.obtener_producto(id_producto)
        if p:
            self.productos.remove(p)
            return True
        return False

    def modificar_producto(self, id_producto: str, nombre: Optional[str] = None,
                           cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        p = self.obtener_producto(id_producto)
        if not p:
            return False
        if nombre is not None:
            p.nombre = nombre
        if cantidad is not None:
            p.cantidad = int(cantidad)
        if precio is not None:
            p.precio = float(precio)
        return True

    def listar_productos(self) -> List[Producto]:
        return list(self.productos)

    def obtener_producto(self, id_producto: str) -> Optional[Producto]:
        for p in self.productos:
            if p.id == str(id_producto):
                return p
        return None

    # Persistencia CSV simple
    def guardar_csv(self, ruta: str) -> None:
        f: TextIO
        with open(ruta, mode="w", newline='', encoding='utf-8') as f:
            writer: DictWriter | Any = csv.DictWriter(f, fieldnames=["id", "nombre", "cantidad", "precio"])
            writer.writeheader()
            for p in self.productos:
                writer.writerow(p.to_dict())

    def cargar_csv(self, ruta: str) -> None:
        try:
            with open(ruta, mode="r", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.productos = [Producto.from_dict(row) for row in reader]
        except FileNotFoundError:
            # archivo no existe: iniciamos vacío
            self.productos = []


# ------------------------------
# archivo: main.py

import tkinter as tk
from tkinter import ttk, messagebox
import inventario


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.inventario = inventario.Inventario()

        # Datos del estudiante
        info_frame = tk.Frame(root, pady=10)
        info_frame.pack()

        tk.Label(info_frame, text="Nombre: Flor Muñoz", font=("Arial", 12, "bold")).pack()
        tk.Label(info_frame, text="Materia: Programación Orientada a Objetos", font=("Arial", 11)).pack()
        tk.Label(info_frame, text="Carrera: Tecnología de la Información", font=("Arial", 11)).pack()
        tk.Label(info_frame, text="Paralelo: A", font=("Arial", 11)).pack()

        # Menú principal
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        menu_productos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=menu_productos)
        menu_productos.add_command(label="Productos", command=self.abrir_productos)
        menu_productos.add_separator()
        menu_productos.add_command(label="Salir", command=root.quit)

    def abrir_productos(self):
        productos_win = tk.Toplevel(self.root)
        productos_win.title("Gestión de Productos")

        frame = tk.Frame(productos_win, pady=10)
        frame.pack()

        # Campos de entrada
        tk.Label(frame, text="ID:").grid(row=0, column=0)
        entry_id = tk.Entry(frame)
        entry_id.grid(row=0, column=1)

        tk.Label(frame, text="Nombre:").grid(row=1, column=0)
        entry_nombre = tk.Entry(frame)
        entry_nombre.grid(row=1, column=1)

        tk.Label(frame, text="Cantidad:").grid(row=2, column=0)
        entry_cantidad = tk.Entry(frame)
        entry_cantidad.grid(row=2, column=1)

        tk.Label(frame, text="Precio:").grid(row=3, column=0)
        entry_precio = tk.Entry(frame)
        entry_precio.grid(row=3, column=1)

        # TreeView
        tree = ttk.Treeview(productos_win, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Precio", text="Precio")
        tree.pack(pady=10)

        # Funciones CRUD
        def actualizar_tabla():
            for row in tree.get_children():
                tree.delete(row)
            for p in self.inventario.productos.values():
                tree.insert("", "end", values=(p.id, p.nombre, p.cantidad, p.precio))

        def agregar():
            try:
                producto = Producto(entry_id.get(), entry_nombre.get(), int(entry_cantidad.get()),
                                    float(entry_precio.get()))
                self.inventario.agregar_producto(producto)
                actualizar_tabla()
                self.inventario.guardar()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def eliminar():
            seleccionado = tree.selection()
            if seleccionado:
                item = tree.item(seleccionado)
                producto_id = item['values'][0]
                assert isinstance(self.inventario.eliminar_producto, object)
                self.inventario.eliminar_producto(producto_id)
                actualizar_tabla()
                self.inventario.guardar()

        def modificar():
            seleccionado = tree.selection()
            if seleccionado:
                item = tree.item(seleccionado)
                producto_id = item['values'][0]
                self.inventario.modificar_producto(producto_id, entry_nombre.get(), int(entry_cantidad.get()),
                                                   float(entry_precio.get()))
                actualizar_tabla()
                self.inventario.guardar()

        # Botones
        tk.Button(frame, text="Agregar", command=agregar).grid(row=4, column=0, pady=5)
        tk.Button(frame, text="Modificar", command=modificar).grid(row=4, column=1, pady=5)
        tk.Button(frame, text="Eliminar", command=eliminar).grid(row=4, column=2, pady=5)

        # Atajos de teclado
        productos_win.bind("<Delete>", lambda e: eliminar())
        productos_win.bind("d", lambda e: eliminar())
        self.root.bind("<Escape>", lambda e: self.root.quit())

        actualizar_tabla()


if __name__ != "__main__":
    pass
else:
    root = tk.Tk()
    app = App(root)
    root.mainloop()
