#TAREA: APLICACION DE CONCEPTOS DE POO EN PYTHON (SEMANA 6)
# Clase base: Animal
class Animal:
    def __init__(self, nombre, edad):
        self.nombre = nombre      # atributo público
        self.__edad = edad        # atributo encapsulado

    def hacer_sonido(self):
        return "Sonido genérico"

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Edad: {self.__edad} años")

    def get_edad(self):  # Método getter
        return self.__edad

    def set_edad(self, nueva_edad):  # Método setter
        if nueva_edad > 0:
            self.__edad = nueva_edad
        else:
            print("Edad no válida")

# Clase derivada: Perro (hereda de Animal)
class Perro(Animal):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)
        self.raza = raza

    # Polimorfismo: sobrescribimos el método hacer_sonido
    def hacer_sonido(self):
        return "Guau guau"

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Raza: {self.raza}")

# Clase derivada: Gato (hereda de Animal)
class Gato(Animal):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color

    # Polimorfismo: sobrescribimos el método hacer_sonido
    def hacer_sonido(self):
        return "Miau"

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Color: {self.color}")

# ==========================
# 👇 Código de prueba 👇
# ==========================

# Crear instancias
animal_generico = Animal("Animalito", 4)
perro1 = Perro("Max", 5, "Labrador")
gato1 = Gato("Michi", 3, "Blanco")

# Llamar métodos
print(">> Animal genérico:")
animal_generico.mostrar_info()
print("Sonido:", animal_generico.hacer_sonido())

print("\n>> Perro:")
perro1.mostrar_info()
print("Sonido:", perro1.hacer_sonido())

print("\n>> Gato:")
gato1.mostrar_info()
print("Sonido:", gato1.hacer_sonido())

# Encapsulación: acceder mediante getter y setter
print("\n>> Cambiando la edad del gato...")
print("Edad actual:", gato1.get_edad())
gato1.set_edad(4)
print("Nueva edad:", gato1.get_edad())

# Intentar poner una edad inválida
gato1.set_edad(-2)  # No se debe permitir
