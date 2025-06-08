from abc import ABC, abstractmethod

# ========== ABSTRACCIÓN ==========
class Animal(ABC):
    def __init__(self, nombre, energia):
        self._nombre = nombre       # Encapsulado con "_"
        self._energia = energia     # Encapsulado con "_"

    def mostrar_estado(self):
        print(f"{self._nombre} - Energía: {self._energia}")

    @abstractmethod
    def hacer_sonido(self):
        pass

    @abstractmethod
    def moverse(self):
        pass

# ========== HERENCIA + POLIMORFISMO ==========
class Perro(Animal):
    def hacer_sonido(self):
        print(f"{self._nombre} dice: ¡Guau!")

    def moverse(self):
        print(f"{self._nombre} corre emocionadamente feliz")
        self._gastar_energia(10)

    def buscar_pelota(self):
        print(f"{self._nombre} está corriendo en el parque")
        self._gastar_energia(5)

    def _gastar_energia(self, param):
        pass


class Pajaro(Animal):
    def hacer_sonido(self):
        print(f"{self._nombre} dice: ¡Pío!")

    def moverse(self):
        print(f"{self._nombre} vuela por el bosque")
        self._gastar_energia(8)

    def construir_nido(self):
        print(f"{self._nombre} está construyendo un nido")
        self._gastar_energia(12)

# ========== ENCAPSULACIÓN ==========
    # Método_privado para controlar el gasto de energía
    def _gastar_energia(self, cantidad):
        self._energia -= cantidad
        if self._energia < 0:
            self._energia = 0

# ========== USO DE LOS OBJETOS ==========
def actividad_animales(animals):
    for animal in animals:
        animal.hacer_sonido()
        animal.moverse()
        animal.mostrar_estado()
        print("-" * 30)

# Creamos instancias
perro = Perro("Riki", 100)
pajaro = Pajaro("Linda", 80)

animales = [perro, pajaro]
actividad_animales(animales)