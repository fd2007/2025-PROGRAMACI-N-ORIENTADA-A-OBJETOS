#SEMANA 13. TAREA (CREACIÓN DE UNA APLICACIÓN GUI BÁSICA)
#NOMBRE: FLOR MUÑOZ

import tkinter as tk
from tkinter import messagebox


# Clase principal de la aplicación
class AplicacionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Datos - Ejemplo GUI Básica")
        self.root.geometry("400x400")  # Tamaño de la ventana

        # --- Sección de diseño ---
        # Etiqueta de título
        self.label_titulo = tk.Label(root, text="Gestor de Datos", font=("Arial", 14, "bold"))
        self.label_titulo.pack(pady=10)

        # Etiqueta y campo de texto
        self.label_ingreso = tk.Label(root, text="Ingrese un dato:")
        self.label_ingreso.pack()

        self.entry_dato = tk.Entry(root, width=30)
        self.entry_dato.pack(pady=5)

        # Botones
        self.btn_agregar = tk.Button(root, text="Agregar", width=10, command=self.agregar_dato)
        self.btn_agregar.pack(pady=5)

        self.btn_limpiar = tk.Button(root, text="Limpiar", width=10, command=self.limpiar_lista)
        self.btn_limpiar.pack(pady=5)

        # Lista para mostrar datos
        self.label_lista = tk.Label(root, text="Datos agregados:")
        self.label_lista.pack(pady=10)

        self.lista_datos = tk.Listbox(root, width=40, height=10)
        self.lista_datos.pack()

    # --- Funcionalidades ---
    def agregar_dato(self):
        """Agrega el dato ingresado en el campo de texto a la lista."""
        dato = self.entry_dato.get().strip()
        if dato:
            self.lista_datos.insert(tk.END, dato)  # Insertar al final de la lista
            self.entry_dato.delete(0, tk.END)  # Limpiar campo de entrada
        else:
            messagebox.showwarning("Atención", "El campo no puede estar vacío.")

    def limpiar_lista(self):
        """Limpia toda la lista de datos."""
        self.lista_datos.delete(0, tk.END)


# --- Programa principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()
