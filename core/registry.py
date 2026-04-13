import tkinter as tk
from tkinter import ttk

# Diccionario maestro de widgets soportados
# Formato: "Nombre Visual": { "class": ClaseTkinter, "icon": "emoji_o_path" }
WIDGET_CATALOG = {
    "Botón": {"class": ttk.Button, "icon": "🔘"},
    "Etiqueta": {"class": ttk.Label, "icon": "📝"},
    "Entrada": {"class": ttk.Entry, "icon": "⌨️"},
    "Contenedor": {"class": tk.Frame, "icon": "📦"},
    "Check": {"class": ttk.Checkbutton, "icon": "✅"},
    "Radio": {"class": ttk.Radiobutton, "icon": "🔘"},
    "Combo": {"class": ttk.Combobox, "icon": "🔽"},
    "Texto": {"class": tk.Text, "icon": "📄"},
    "Progreso": {"class": ttk.Progressbar, "icon": "⏳"},
    "Scroll": {"class": ttk.Scrollbar, "icon": "📜"},
    "Separador": {"class": ttk.Separator, "icon": "➖"},
}


def get_widget_class(name):
    return WIDGET_CATALOG.get(name, {}).get("class", tk.Label)


def get_supported_props(class_name):
    # Retorna las propiedades editables según la clase
    for item in WIDGET_CATALOG.values():
        if item["class"].__name__ == class_name:
            return item.get("props", ["text"])
    return ["text"]
