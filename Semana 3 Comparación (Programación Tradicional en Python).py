#PROGRAMACIÓN_TRADICIONAL
def pedir_temperaturas():
    print("Ingrese las temperaturas de cada día de la semana:")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    temperaturas = []
    for dia in dias:
        temp = float(input(f"{dia}: "))
        temperaturas.append(temp)
    return temperaturas

def promedio_semanal(temps):
    return round(sum(temps) / len(temps), 2)

# Programa principal
temps = pedir_temperaturas()
prom = promedio_semanal(temps)
print(f"\nEl promedio de la semana fue: {prom}°C")
