#PROGRAMACIÓN_ORIENTADA_A_OBJETOS
class SemanClima:
    def __init__(self):
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.temperaturas = []

    def ingresar_temperaturas(self):
        print("Registre la temperatura para cada día:")
        for dia in self.dias:
            temp = float(input(f"{dia}: "))
            self.temperaturas.append(temp)

    def promedio(self):
        if self.temperaturas:
            return round(sum(self.temperaturas) / len(self.temperaturas), 2)
        return 0.0

    def mostrar_promedio(self):
        print(f"\nTemperatura promedio de la semana: {self.promedio()}°C")

# Ejecutar
semana = SemanClima()
semana.ingresar_temperaturas()
semana.mostrar_promedio()
