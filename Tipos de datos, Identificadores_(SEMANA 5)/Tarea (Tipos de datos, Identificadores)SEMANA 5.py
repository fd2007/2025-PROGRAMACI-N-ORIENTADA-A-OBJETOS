# TAREA SEMANA 5. TEMA: Tarea: Tipos de datos, Identificadores.
# Este programa convierte una temperatura dada en grados Celsius a Fahrenheit y Kelvin.
# Demuestra el uso de diferentes tipos de datos, identificadores descriptivos y convenciones de estilo en Python.

def convertir_temperatura(celsius):
    """Convierte grados Celsius a Fahrenheit y Kelvin"""
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15
    return fahrenheit, kelvin

# Entrada del usuario
temperatura_celsius = float(input("Ingresa la temperatura en grados Celsius: "))

# Conversión
temperatura_fahrenheit, temperatura_kelvin = convertir_temperatura(temperatura_celsius)

# Salida
print("Temperatura en Fahrenheit:", temperatura_fahrenheit)
print("Temperatura en Kelvin:", temperatura_kelvin)

# Variables booleanas para verificar si la temperatura es alta o baja
es_frio = temperatura_celsius < 10
es_calor = temperatura_celsius > 30

# Mensaje adicional
if es_frio:
    print("Esta Haciendo frío.")
elif es_calor:
    print("Esta haciendo calor.")
else:
    print("La temperatura es agradable.")
