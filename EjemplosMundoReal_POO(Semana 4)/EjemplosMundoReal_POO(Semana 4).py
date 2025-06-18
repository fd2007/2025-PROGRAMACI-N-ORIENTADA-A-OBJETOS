# Semana 4
# tienda_libros.py

# Clase que representa un Libro
class Libro:
    def __init__(self, titulo, autor, precio):
        self.titulo = titulo
        self.autor = autor
        self.precio = precio

    def mostrar_info(self):
        print(f"'{self.titulo}' por {self.autor}, Precio: ${self.precio:.2f}")

# Clase que representa una Tienda de Libros
class Tienda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = []

    def agregar_libro(self, libro):
        self.inventario.append(libro)
        print(f"Libro agregado: {libro.titulo}")

    def mostrar_inventario(self):
        print(f"\nInventario de {self.nombre}:")
        if not self.inventario:
            print("No hay libros en el inventario.")
        for libro in self.inventario:
            libro.mostrar_info()

    def buscar_libro(self, titulo):
        for libro in self.inventario:
            if libro.titulo.lower() == titulo.lower():
                print("\nLibro encontrado:")
                libro.mostrar_info()
                return
        print("Libro no encontrado.")

# Uso de las clases
if __name__ == "__main__":
    tienda = Tienda("Librería Mundo Lectura")

    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 19.99)
    libro2 = Libro("1984", "George Orwell", 15.50)
    libro3 = Libro("Don Quijote", "Miguel de Cervantes", 22.00)

    tienda.agregar_libro(libro1)
    tienda.agregar_libro(libro2)
    tienda.agregar_libro(libro3)

    tienda.mostrar_inventario()
    tienda.buscar_libro("1984")
