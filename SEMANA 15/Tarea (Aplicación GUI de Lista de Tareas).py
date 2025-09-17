# SEMANA 15 TAREA: APLICACIÓN GUI DE LISTA DE TAREAS
# NOMBRE: FLOR MUÑOZ
import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Original")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Marco superior: entrada + botón añadir
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack()

        self.task_var = tk.StringVar()
        self.entry_task = tk.Entry(frame_top, textvariable=self.task_var, width=30)
        self.entry_task.pack(side=tk.LEFT, padx=5)
        self.entry_task.bind("<Return>", self.add_task)  # Enter agrega tarea

        btn_add = tk.Button(frame_top, text="➕ Añadir", command=self.add_task)
        btn_add.pack(side=tk.LEFT)

        # Lista con scrollbar
        frame_list = tk.Frame(self.root)
        frame_list.pack(pady=5)

        self.scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            frame_list,
            width=45,
            height=12,
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT)

        # Eventos adicionales
        self.listbox.bind("<Double-Button-1>", self.toggle_complete)  # Doble clic
        self.listbox.bind("<Delete>", self.delete_task)              # Tecla Supr

        # Botones inferiores
        frame_bottom = tk.Frame(self.root, pady=10)
        frame_bottom.pack()

        btn_complete = tk.Button(frame_bottom, text="✔ Marcar Completada", command=self.toggle_complete)
        btn_complete.grid(row=0, column=0, padx=5)

        btn_delete = tk.Button(frame_bottom, text="🗑 Eliminar", command=self.delete_task)
        btn_delete.grid(row=0, column=1, padx=5)

    # ---------------------- Funciones de la app ----------------------

    def add_task(self, event=None):
        """Añade una nueva tarea si el campo no está vacío."""
        task = self.task_var.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.task_var.set("")
        else:
            messagebox.showwarning("Advertencia", "Escribe una tarea antes de añadir.")

    def toggle_complete(self, event=None):
        """Marca o desmarca la tarea seleccionada como completada."""
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            task_text = self.listbox.get(index)

            if task_text.startswith("✔ "):
                # Si ya estaba completada, la dejamos normal
                new_text = task_text[2:]
            else:
                # La marcamos como completada
                new_text = "✔ " + task_text

            self.listbox.delete(index)
            self.listbox.insert(index, new_text)

    def delete_task(self, event=None):
        """Elimina la tarea seleccionada."""
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected[0])
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminar.")


# ---------------------- Programa Principal ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
