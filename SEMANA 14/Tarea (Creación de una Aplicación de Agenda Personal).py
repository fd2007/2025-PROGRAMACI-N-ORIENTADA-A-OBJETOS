# SEMANA 14 (TAREA: CREACIÓN DE UNA APLICACIÓN DE AGENDA PERSONAL)
# NOMBRE: FLOR MUÑOZ

"""
Agenda Personal - Aplicación GUI con Tkinter

Características:
- Ventana principal con TreeView que muestra eventos (fecha, hora, descripción).
- Campos de entrada para fecha, hora y descripción.
- DatePicker con tkcalendar.DateEntry cuando esté disponible; si no, se usa Entry con formato 'YYYY-MM-DD'.
- Botones: Agregar Evento, Eliminar Evento Seleccionado (con confirmación), Salir.
- Organización usando Frames.
- Persistencia opcional en 'events.json' (guarda/recarga eventos).

Requisitos:
- Python 3.8+
- Recomendado instalar: pip install tkcalendar (opcional, mejora selección de fecha)

Ejecutar:
python agenda_personal_tkinter.py

"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# Intentar usar DateEntry (tkcalendar). Si no está disponible, usar Entry como fallback.
try:
    from tkcalendar import DateEntry
    HAVE_TKCALENDAR = True
except Exception:
    HAVE_TKCALENDAR = False

DATA_FILE = "events.json"


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("700x450")
        self.resizable(False, False)

        # Contenedores (Frames)
        self.tree_frame = ttk.Frame(self, padding=(10, 10))
        self.input_frame = ttk.Frame(self, padding=(10, 0))
        self.action_frame = ttk.Frame(self, padding=(10, 10))

        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.input_frame.pack(fill=tk.X)
        self.action_frame.pack(fill=tk.X)

        # TreeView (lista de eventos)
        self.tree = ttk.Treeview(self.tree_frame, columns=("date", "time", "desc"), show="headings", selectmode="browse")
        self.tree.heading("date", text="Fecha")
        self.tree.heading("time", text="Hora")
        self.tree.heading("desc", text="Descripción")
        self.tree.column("date", width=120, anchor=tk.CENTER)
        self.tree.column("time", width=80, anchor=tk.CENTER)
        self.tree.column("desc", width=420, anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)

        # Input fields labels + widgets (organizados con grid dentro de input_frame)
        ttk.Label(self.input_frame, text="Fecha:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        ttk.Label(self.input_frame, text="Hora (HH:MM):").grid(row=0, column=2, padx=5, pady=8, sticky=tk.W)
        ttk.Label(self.input_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=4, sticky=tk.W)

        # Fecha: DateEntry si existe, sino Entry con placeholder formato
        if HAVE_TKCALENDAR:
            self.date_entry = DateEntry(self.input_frame, date_pattern='yyyy-mm-dd')
        else:
            self.date_entry = ttk.Entry(self.input_frame)
            self.date_entry.insert(0, "YYYY-MM-DD")

        self.date_entry.grid(row=0, column=1, padx=5, pady=8, sticky=tk.W)

        # Hora
        self.time_entry = ttk.Entry(self.input_frame, width=10)
        self.time_entry.grid(row=0, column=3, padx=5, pady=8, sticky=tk.W)

        # Descripción (Entry amplio)
        self.desc_entry = ttk.Entry(self.input_frame, width=60)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=4, sticky=tk.W)

        # Botones
        add_btn = ttk.Button(self.action_frame, text="Agregar Evento", command=self.add_event)
        del_btn = ttk.Button(self.action_frame, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        exit_btn = ttk.Button(self.action_frame, text="Salir", command=self.on_exit)

        add_btn.pack(side=tk.LEFT, padx=(0, 8))
        del_btn.pack(side=tk.LEFT, padx=(0, 8))
        exit_btn.pack(side=tk.RIGHT)

        # Cargar eventos previos
        self.events = []  # lista de dicts: {"date":..., "time":..., "desc":...}
        self.load_events()
        self.refresh_treeview()

        # Bind doble click para editar (opcional - aquí abriremos una ventana para editar)
        self.tree.bind("<Double-1>", self.on_double_click)

    def validate_date(self, date_text):
        try:
            # aceptar formato YYYY-MM-DD
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def validate_time(self, time_text):
        try:
            # aceptar formato HH:MM (24 horas)
            datetime.strptime(time_text, "%H:%M")
            return True
        except Exception:
            return False

    def add_event(self):
        date_text = self.date_entry.get().strip()
        time_text = self.time_entry.get().strip()
        desc_text = self.desc_entry.get().strip()

        # Validaciones
        if not date_text or not time_text or not desc_text:
            messagebox.showwarning("Campos incompletos", "Por favor rellena Fecha, Hora y Descripción.")
            return

        if not self.validate_date(date_text):
            messagebox.showerror("Fecha inválida", "La fecha debe tener el formato YYYY-MM-DD.")
            return

        if not self.validate_time(time_text):
            messagebox.showerror("Hora inválida", "La hora debe tener el formato HH:MM (24 horas). Ej: 14:30")
            return

        # Añadir evento
        event = {"date": date_text, "time": time_text, "desc": desc_text}
        self.events.append(event)

        # Ordenar eventos por fecha y hora
        try:
            self.events.sort(key=lambda e: datetime.strptime(e['date'] + ' ' + e['time'], '%Y-%m-%d %H:%M'))
        except Exception:
            pass

        self.refresh_treeview()
        self.save_events()

        # Limpiar campos (mantener la fecha en DateEntry si existe)
        if not HAVE_TKCALENDAR:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, "YYYY-MM-DD")
        self.time_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def delete_selected_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecciona un evento", "Por favor selecciona el evento que deseas eliminar.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        fecha, hora, desc = values

        # Confirmación
        if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el evento:\n{fecha} {hora} - {desc} ?"):
            # Encontrar y eliminar de self.events (el primer match)
            for i, ev in enumerate(self.events):
                if ev['date'] == fecha and ev['time'] == hora and ev['desc'] == desc:
                    del self.events[i]
                    break
            self.refresh_treeview()
            self.save_events()

    def on_exit(self):
        self.save_events()
        self.destroy()

    def refresh_treeview(self):
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insertar
        for ev in self.events:
            self.tree.insert('', tk.END, values=(ev['date'], ev['time'], ev['desc']))

    def load_events(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
            except Exception:
                self.events = []
        else:
            self.events = []

    def save_events(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar los eventos.\n{e}")

    def on_double_click(self, event):
        # Abrir diálogo simple para ver/editar el evento doble clickeado
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        fecha, hora, desc = self.tree.item(item, 'values')
        EditWindow(self, fecha, hora, desc)


class EditWindow(tk.Toplevel):
    def __init__(self, master, fecha, hora, desc):
        super().__init__(master)
        self.title("Editar Evento")
        self.resizable(False, False)
        self.geometry("420x160")

        ttk.Label(self, text="Fecha:").grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)
        ttk.Label(self, text="Hora (HH:MM):").grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)
        ttk.Label(self, text="Descripción:").grid(row=2, column=0, padx=8, pady=8, sticky=tk.W)

        # Fecha campo (DateEntry si está disponible)
        if HAVE_TKCALENDAR:
            self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
            self.date_entry.set_date(fecha)
        else:
            self.date_entry = ttk.Entry(self)
            self.date_entry.insert(0, fecha)

        self.date_entry.grid(row=0, column=1, padx=8, pady=8)
        self.time_entry = ttk.Entry(self, width=10)
        self.time_entry.grid(row=1, column=1, padx=8, pady=8)
        self.time_entry.insert(0, hora)

        self.desc_entry = ttk.Entry(self, width=40)
        self.desc_entry.grid(row=2, column=1, padx=8, pady=8)
        self.desc_entry.insert(0, desc)

        save_btn = ttk.Button(self, text="Guardar cambios", command=self.save_changes)
        cancel_btn = ttk.Button(self, text="Cancelar", command=self.destroy)
        save_btn.grid(row=3, column=0, padx=8, pady=8)
        cancel_btn.grid(row=3, column=1, padx=8, pady=8)

    def save_changes(self):
        new_date = self.date_entry.get().strip()
        new_time = self.time_entry.get().strip()
        new_desc = self.desc_entry.get().strip()

        if not new_date or not new_time or not new_desc:
            messagebox.showwarning("Campos incompletos", "Por favor rellena Fecha, Hora y Descripción.")
            return
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Fecha inválida", "La fecha debe tener el formato YYYY-MM-DD.")
            return
        try:
            datetime.strptime(new_time, "%H:%M")
        except Exception:
            messagebox.showerror("Hora inválida", "La hora debe tener el formato HH:MM (24 horas). Ej: 14:30")
            return

        # Actualizar evento en la lista principal
        master = self.master
        # buscamos el evento con la descripción vieja + fecha + hora y lo actualizamos
        for ev in master.events:
            if ev['date'] == self.date_entry.get() and ev['time'] == self.time_entry.get() and ev['desc'] == self.desc_entry.get():
                # Este bloque en realidad busca, pero como ya cambiamos los campos, mejor buscar usando los valores originales
                pass

        # Para evitar complicaciones, buscaremos por la selección actual en el Treeview
        sel = master.tree.selection()
        if sel:
            item = sel[0]
            old_values = master.tree.item(item, 'values')
            old_date, old_time, old_desc = old_values
            for i, ev in enumerate(master.events):
                if ev['date'] == old_date and ev['time'] == old_time and ev['desc'] == old_desc:
                    master.events[i] = {'date': new_date, 'time': new_time, 'desc': new_desc}
                    break

            # Reordenar y guardar
            try:
                master.events.sort(key=lambda e: datetime.strptime(e['date'] + ' ' + e['time'], '%Y-%m-%d %H:%M'))
            except Exception:
                pass
            master.refresh_treeview()
            master.save_events()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo encontrar el evento a editar.")


if __name__ == '__main__':
    app = AgendaApp()
    app.mainloop()
