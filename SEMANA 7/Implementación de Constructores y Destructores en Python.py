# Clase Libro para demostrar el uso de constructores y destructores en Python
class Libro:
    def __init__(self, titulo, autor):
        """
        Constructor de la clase. Se ejecuta automáticamente al crear un objeto.
        Inicializa los atributos del libro.
        """
        self.titulo = titulo
        self.autor = autor
        print(f"V: Libro creado: '{self.titulo}' por {self.autor}")

    def mostrar_info(self):
        """Método para mostrar información del libro."""
        print(f"El libro '{self.titulo}' fue escrito por {self.autor}.")

    def __del__(self):
        """
        Destructor de la clase. Se ejecuta automáticamente cuando el objeto es eliminado.
        Se usa para realizar limpieza o liberar recursos si es necesario.
        """
        print(f"X: Libro destruido: '{self.titulo}' por {self.autor}")


# Bloque principal del programa
def main():
    # Crear un objeto de la clase Libro
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez")
    libro1.mostrar_info()

    # Otro ejemplo
    libro2 = Libro("1984", "George Orwell")
    libro2.mostrar_info()

    # Eliminar un objeto manualmente (opcional)
    del libro2

    # El destructor de libro1 se llamará automáticamente al final del programa

if __name__ == "__main__":
    main()
