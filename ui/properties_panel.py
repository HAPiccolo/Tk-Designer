# ui/properties_panel.py
import tkinter as tk
from tkinter import ttk


class PropertiesPanel(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Editor de Propiedades", **kwargs)
        self.current_widget = None
        self.entries = {}

    def load_widget(self, widget):
        """Carga las propiedades editables del widget seleccionado."""
        self.current_widget = widget
        # Limpiar panel anterior
        for child in self.winfo_children():
            child.destroy()

        self.entries = {}

        # Propiedades comunes que queremos editar
        props = ["text", "bg", "fg", "width", "height", "font", "cursor"]

        for i, prop in enumerate(props):
            try:
                # Intentamos obtener el valor actual de la propiedad
                current_val = widget.cget(prop)

                ttk.Label(self, text=f"{prop.capitalize()}:").grid(
                    row=i, column=0, sticky="w", padx=5
                )
                entry = ttk.Entry(self)
                entry.insert(0, str(current_val))
                entry.grid(row=i, column=1, fill="x", padx=5, pady=2)

                # Evento para actualizar en tiempo real al presionar Enter
                entry.bind(
                    "<Return>",
                    lambda e, p=prop, en=entry: self._update_prop(p, en.get()),
                )
                self.entries[prop] = entry
            except:
                continue  # Si el widget no tiene esa propiedad, la saltamos

    def _update_prop(self, prop, value):
        if self.current_widget:
            try:
                self.current_widget.config(**{prop: value})
            except Exception as e:
                print(f"Error actualizando {prop}: {e}")
