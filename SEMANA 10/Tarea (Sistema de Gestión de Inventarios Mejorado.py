#Tarea: Sistema de Gestión de Inventarios Mejorado (SEMANA 10)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Inventarios (con archivos y manejo de excepciones)
------------------------------------------------------------------------

Estas son las características clave:
- Persistencia en archivo de texto (CSV dentro de .txt por compatibilidad).
- Carga automática al iniciar. Si no existe el archivo, se crea vacío.
- Manejo de excepciones comunes durante lectura/escritura: FileNotFoundError,
  PermissionError, errores de parseo (archivo corrupto), etc.
- Interfaz de consola con mensajes claros de éxito o fallo.
- Escritura atómica (usa archivo temporal + os.replace) para minimizar corrupción.
- Código comentado y organizado.

Formato del archivo `inventario.txt` (CSV con cabecera):
    id,nombre,cantidad,precio
    P001,Lápiz,120,0.25
    P002,Cuaderno,50,1.80

Run:
    python inventario.py

Autor: (Flor Muñoz)
"""
from __future__ import annotations

import csv
import os
import sys
import tempfile
from dataclasses import dataclass, asdict
from typing import Dict, Optional, Tuple, List


# -----------------------------
# Modelo de dominio
# -----------------------------
@dataclass
class Producto:
    id: str
    nombre: str
    cantidad: int
    precio: float

    def to_row(self) -> Dict[str, str]:
        """Convierte a un dict listo para csv.DictWriter."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": str(self.cantidad),
            "precio": f"{self.precio:.2f}",
        }


# -----------------------------
# Repositorio con persistencia
# -----------------------------
class Inventario:
    """Gestor de inventario respaldado por archivo CSV.

    - Mantiene un índice en memoria (diccionario) para rapidez.
    - En cada operación de escritura (agregar/actualizar/eliminar) sincroniza
      al archivo con escritura atómica.
    - Carga inicial tolerante a fallos: ignora filas inválidas y avisa.
    """

    CAMPOS = ("id", "nombre", "cantidad", "precio")

    def __init__(self, ruta_archivo: str = "inventario.txt") -> None:
        self.ruta_archivo = ruta_archivo
        self._productos: Dict[str, Producto] = {}
        self._solo_lectura = False  # Se activa si detectamos PermissionError al escribir
        self._errores_carga: List[str] = []
        self._asegurar_archivo()
        self._cargar_desde_archivo()

    # ---------------------
    # Utilidades de archivo
    # ---------------------
    def _asegurar_archivo(self) -> None:
        """Crea el archivo si no existe. Maneja permisos y directorios."""
        try:
            carpeta = os.path.dirname(self.ruta_archivo)
            if carpeta and not os.path.exists(carpeta):
                os.makedirs(carpeta, exist_ok=True)
            if not os.path.exists(self.ruta_archivo):
                # Crear archivo con cabecera vacía
                with open(self.ruta_archivo, mode="w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=self.CAMPOS)
                    writer.writeheader()
        except PermissionError:
            print("[ADVERTENCIA] No hay permisos para crear el archivo de inventario. El sistema funcionará en modo solo-lectura.")
            self._solo_lectura = True
        except OSError as e:
            print(f"[ADVERTENCIA] No se pudo crear el archivo de inventario: {e}. Modo solo-lectura activado.")
            self._solo_lectura = True

    def _cargar_desde_archivo(self) -> None:
        """Lee el archivo y reconstruye el inventario en memoria.
        - Si el archivo no existe, intenta crearlo (ya manejado en _asegurar_archivo).
        - Si hay filas corruptas, las salta y acumula mensajes en _errores_carga.
        """
        try:
            with open(self.ruta_archivo, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    # Archivo vacío sin cabecera => reescribimos cabecera
                    self._reescribir_cabecera_por_si_acaso()
                    return
                faltan_campos = [c for c in self.CAMPOS if c not in reader.fieldnames]
                if faltan_campos:
                    self._errores_carga.append(
                        f"Cabecera inválida; faltan: {', '.join(faltan_campos)}. Se ignorará el contenido."
                    )
                    return
                for i, row in enumerate(reader, start=2):  # start=2 por la cabecera en línea 1
                    try:
                        idp = (row.get("id") or "").strip()
                        nombre = (row.get("nombre") or "").strip()
                        cantidad_str = (row.get("cantidad") or "0").strip()
                        precio_str = (row.get("precio") or "0").strip()
                        if not idp:
                            raise ValueError("ID vacío")
                        cantidad = int(cantidad_str)
                        precio = float(precio_str)
                        self._productos[idp] = Producto(id=idp, nombre=nombre, cantidad=cantidad, precio=precio)
                    except Exception as e:  # captura parseos erróneos
                        self._errores_carga.append(f"Línea {i}: {e}. Fila ignorada.")
        except FileNotFoundError:
            # Ya lo gestiona _asegurar_archivo; aquí lo informamos por consola.
            print("[INFO] inventario.txt no existía; se creará uno nuevo.")
            self._asegurar_archivo()
        except PermissionError:
            print("[ERROR] No hay permisos para leer el archivo de inventario. El sistema funcionará con inventario vacío.")
            self._solo_lectura = True
        except OSError as e:
            print(f"[ERROR] No se pudo leer el archivo de inventario: {e}. Se inicializa inventario vacío.")

    def _reescribir_cabecera_por_si_acaso(self) -> None:
        """Si el archivo está vacío o sin cabecera, escribe cabecera sin perder datos (no hay datos)."""
        try:
            if self._solo_lectura:
                return
            with open(self.ruta_archivo, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.CAMPOS)
                writer.writeheader()
        except PermissionError:
            print("[ADVERTENCIA] No hay permisos para escribir cabecera en el archivo. Modo solo-lectura.")
            self._solo_lectura = True
        except OSError as e:
            print(f"[ADVERTENCIA] Error reescribiendo cabecera: {e}")

    def _guardar_atomico(self) -> bool:
        """Escribe todo el inventario a disco usando escritura atómica.
        Devuelve True si se guardó correctamente, False en caso de error.
        """
        if self._solo_lectura:
            print("[ADVERTENCIA] El sistema está en modo solo-lectura; no se puede guardar en archivo.")
            return False
        try:
            carpeta = os.path.dirname(self.ruta_archivo) or "."
            with tempfile.NamedTemporaryFile("w", delete=False, dir=carpeta, encoding="utf-8", newline="") as tmp:
                tmp_ruta = tmp.name
                writer = csv.DictWriter(tmp, fieldnames=self.CAMPOS)
                writer.writeheader()
                for p in self._productos.values():
                    writer.writerow(p.to_row())
            os.replace(tmp_ruta, self.ruta_archivo)  # atómico en la mayoría de SO
            return True
        except PermissionError:
            print("[ERROR] Permiso denegado al escribir el archivo de inventario. Cambiando a modo solo-lectura.")
            self._solo_lectura = True
            return False
        except OSError as e:
            print(f"[ERROR] No se pudo escribir el archivo de inventario: {e}")
            return False

    # ---------------------
    # Operaciones de negocio
    # ---------------------
    def agregar(self, producto: Producto) -> Tuple[bool, str]:
        if producto.id in self._productos:
            return False, f"Ya existe un producto con ID '{producto.id}'."
        self._productos[producto.id] = producto
        if self._guardar_atomico():
            return True, f"Producto '{producto.nombre}' agregado y guardado en archivo."
        else:
            return False, "Producto agregado en memoria, pero falló la escritura en archivo."

    def actualizar(self, id_producto: str, *, nombre: Optional[str] = None,
                   cantidad: Optional[int] = None, precio: Optional[float] = None) -> Tuple[bool, str]:
        p = self._productos.get(id_producto)
        if not p:
            return False, f"No existe producto con ID '{id_producto}'."
        if nombre is not None:
            p.nombre = nombre
        if cantidad is not None:
            if cantidad < 0:
                return False, "La cantidad no puede ser negativa."
            p.cantidad = cantidad
        if precio is not None:
            if precio < 0:
                return False, "El precio no puede ser negativo."
            p.precio = precio
        if self._guardar_atomico():
            return True, f"Producto '{id_producto}' actualizado y guardado en archivo."
        else:
            return False, "Producto actualizado en memoria, pero falló la escritura en archivo."

    def eliminar(self, id_producto: str) -> Tuple[bool, str]:
        if id_producto not in self._productos:
            return False, f"No existe producto con ID '{id_producto}'."
        eliminado = self._productos.pop(id_producto)
        if self._guardar_atomico():
            return True, f"Producto '{eliminado.nombre}' eliminado y cambios guardados en archivo."
        else:
            return False, "Producto eliminado en memoria, pero falló la escritura en archivo."

    def obtener(self, id_producto: str) -> Optional[Producto]:
        return self._productos.get(id_producto)

    def listar(self) -> List[Producto]:
        return list(self._productos.values())

    # ---------------------
    # Info de estado
    # ---------------------
    def errores_carga(self) -> List[str]:
        return list(self._errores_carga)

    def es_solo_lectura(self) -> bool:
        return self._solo_lectura


# --------------------------------------
# Interfaz de usuario (consola interact.)
# --------------------------------------

def pedir_no_vacio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("⚠️  No puede estar vacío.")


def pedir_entero(msg: str) -> int:
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except ValueError:
            print("⚠️  Debe ser un número entero válido.")


def pedir_flotante(msg: str) -> float:
    while True:
        s = input(msg).strip()
        try:
            return float(s)
        except ValueError:
            print("⚠️  Debe ser un número (ej. 10, 10.5).")


def imprimir_tabla(productos: List[Producto]) -> None:
    if not productos:
        print("(Inventario vacío)")
        return
    ancho_id = max(2, max(len(p.id) for p in productos))
    ancho_nombre = max(6, max(len(p.nombre) for p in productos))
    print(f"{'ID'.ljust(ancho_id)}  {'Nombre'.ljust(ancho_nombre)}  Cantidad  Precio")
    print("-" * (ancho_id + ancho_nombre + 21))
    for p in productos:
        print(f"{p.id.ljust(ancho_id)}  {p.nombre.ljust(ancho_nombre)}  {str(p.cantidad).rjust(8)}  {p.precio:>7.2f}")


def menu() -> None:
    print("""
==============================
 Sistema de Inventario (Archivo)
==============================
[1] Agregar producto
[2] Actualizar producto
[3] Eliminar producto
[4] Listar productos
[5] Buscar producto por ID
[6] Ver estado del archivo
[7] Ejecutar pruebas rápidas
[0] Salir
""")


def ejecutar_pruebas_rapidas() -> None:
    """Realiza una batería simple de pruebas en un archivo temporal dentro de ./tmp_test.
    No sustituye pruebas unitarias formales, pero ayuda a verificar escenarios comunes,
    incluyendo archivo corrupto y permisos simulados.
    """
    print("\n[PRUEBAS] Iniciando pruebas rápidas...")
    carpeta = "tmp_test"
    os.makedirs(carpeta, exist_ok=True)
    ruta_temp = os.path.join(carpeta, "inventario_pruebas.txt")

    # 1) Archivo inexistente (se debe crear solo)
    if os.path.exists(ruta_temp):
        os.remove(ruta_temp)
    inv = Inventario(ruta_temp)
    assert len(inv.listar()) == 0, "Debe iniciar vacío"

    ok, msg = inv.agregar(Producto("T001", "Teclado", 10, 19.99))
    print("- Agregar:", msg)
    assert ok

    ok, msg = inv.actualizar("T001", cantidad=15)
    print("- Actualizar:", msg)
    assert ok

    ok, msg = inv.eliminar("T001")
    print("- Eliminar:", msg)
    assert ok

    # 2) Archivo corrupto (líneas inválidas)
    with open(ruta_temp, "w", encoding="utf-8") as f:
        f.write("id,nombre,cantidad,precio\n")
        f.write("X01,ItemBien,5,1.50\n")
        f.write("X02,ItemMal,cantidad_no_numero,3.0\n")  # corrupto
        f.write(",,10,\n")  # corrupto (id vacío)

    inv2 = Inventario(ruta_temp)
    errores = inv2.errores_carga()
    print("- Errores detectados en carga (esperado > 0):")
    for e in errores:
        print("   ", e)
    assert any("Línea" in e for e in errores), "Debe reportar líneas corruptas"
    assert inv2.obtener("X01") is not None

    # 3) Simular permiso denegado (solo lectura) => en muchas plataformas no podemos
    # cambiar permisos de forma portable aquí; mostramos cómo probar manualmente:
    print("\n[PRUEBAS] Para probar PermissionError manualmente:")
    print("   - En Linux/Mac: cambiar permisos del archivo o carpeta a solo lectura.")
    print("   - En Windows: marcar el archivo como 'Solo lectura' desde propiedades.")
    print("   - Luego intentar agregar/actualizar y observar el mensaje de error.")

    print("[PRUEBAS] Finalizadas.\n")


# -----------------------------
# Punto de entrada (CLI)
# -----------------------------

def main() -> None:
    ruta = "inventario.txt"  # puedes cambiarlo o parametrizar con sys.argv
    inv = Inventario(ruta)

    # Informar estado inicial y errores de carga
    if inv.errores_carga():
        print("\n[AVISO] Durante la carga se detectaron problemas en el archivo:")
        for e in inv.errores_carga():
            print("   -", e)
    print(f"[INFO] Productos cargados: {len(inv.listar())}. Archivo: {ruta}")
    if inv.es_solo_lectura():
        print("[MODO] Solo-lectura ACTIVADO por problemas de permisos.\n")

    while True:
        try:
            menu()
            opcion = input("Elige una opción: ").strip()
            if opcion == "0":
                print("Saliendo... ¡Hasta pronto!")
                break
            elif opcion == "1":
                idp = pedir_no_vacio("ID: ")
                nombre = pedir_no_vacio("Nombre: ")
                cantidad = pedir_entero("Cantidad: ")
                precio = pedir_flotante("Precio: ")
                ok, msg = inv.agregar(Producto(idp, nombre, cantidad, precio))
                print(("✅ " if ok else "❌ ") + msg)
            elif opcion == "2":
                idp = pedir_no_vacio("ID del producto a actualizar: ")
                print("Presiona Enter para dejar sin cambio.")
                nombre = input("Nuevo nombre: ").strip() or None
                cant_s = input("Nueva cantidad: ").strip()
                pre_s = input("Nuevo precio: ").strip()
                cantidad = int(cant_s) if cant_s else None
                precio = float(pre_s) if pre_s else None
                ok, msg = inv.actualizar(idp, nombre=nombre, cantidad=cantidad, precio=precio)
                print(("✅ " if ok else "❌ ") + msg)
            elif opcion == "3":
                idp = pedir_no_vacio("ID del producto a eliminar: ")
                ok, msg = inv.eliminar(idp)
                print(("✅ " if ok else "❌ ") + msg)
            elif opcion == "4":
                imprimir_tabla(inv.listar())
            elif opcion == "5":
                idp = pedir_no_vacio("ID a buscar: ")
                p = inv.obtener(idp)
                if p:
                    imprimir_tabla([p])
                else:
                    print("❌ No se encontró el producto.")
            elif opcion == "6":
                print(f"Archivo: {inv.ruta_archivo}")
                print(f"Solo-lectura: {inv.es_solo_lectura()}")
                if inv.errores_carga():
                    print("Errores de carga:")
                    for e in inv.errores_carga():
                        print("  -", e)
                else:
                    print("Sin errores de carga registrados.")
            elif opcion == "7":
                ejecutar_pruebas_rapidas()
            else:
                print("Opción no válida.")
        except PermissionError:
            # Errores inesperados de permisos en operaciones I/O puntuales
            print("❌ Error de permisos al acceder al sistema de archivos.")
        except KeyboardInterrupt:
            print("\nInterrupción recibida. Saliendo...")
            break
        except Exception as e:
            # Evita que errores no controlados derriben el programa
            print(f"❌ Ocurrió un error no esperado: {e}")


if __name__ == "__main__":
    main()
