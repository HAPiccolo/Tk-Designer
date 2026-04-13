import tkinter as tk
import json
import os


class TKDLoader:
    def __init__(self, master, file_path):
        self.master = master
        self.widgets = {}

        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self._build_interface()

    def _build_interface(self):
        # Mapeo manual: Si el JSON dice TButton, usamos tk.Button
        MAPEO = {
            "TButton": tk.Button,
            "TLabel": tk.Label,
            "TEntry": tk.Entry,
            "TCheckbutton": tk.Checkbutton,
            "Frame": tk.Frame,
            "Button": tk.Button,
            "Label": tk.Label,
            "Entry": tk.Entry,
        }

        # 1. Separar Frames para el fondo
        frames = [i for i in self.data if "Frame" in i.get("type", "")]
        others = [i for i in self.data if "Frame" not in i.get("type", "")]

        for item in frames + others:
            w_type = item["type"]
            w_id = item["id"]

            # Obtener la clase de tk usando el mapeo
            cls = MAPEO.get(w_type)

            if not cls:
                print(f"⚠️ Saltando '{w_type}': No está en el mapeo de tk.")
                continue

            # Crear el widget (Todos hijos del master/root directamente)
            obj = cls(self.master)

            # Configuración de propiedades
            config = {}
            if "text" in item:
                config["text"] = item["text"]
            if "bg" in item:
                config["bg"] = item["bg"]

            try:
                obj.config(**config)
            except:
                pass

            # Posicionamiento (Place)
            obj.place(
                x=int(item["x"]),
                y=int(item["y"]),
                width=int(item.get("width", 100)),
                height=int(item.get("height", 35)),
            )

            # Forzar visibilidad
            obj.lift()
            self.widgets[w_id] = obj
            print(f"✅ OK: {w_id} ({w_type} -> {cls.__name__})")

    def connect(self, widget_id, function, event="<Button-1>"):
        if widget_id in self.widgets:
            w = self.widgets[widget_id]
            if hasattr(w, "config") and "command" in w.keys():
                w.config(command=function)
            else:
                w.bind(event, lambda e: function())

    def get_value(self, widget_id):
        w = self.widgets.get(widget_id)
        return w.get() if w and hasattr(w, "get") else ""
