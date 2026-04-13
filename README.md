# TK-Designer 🎨 🐍

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)](#)

**TK-Designer** es un ecosistema ligero para el desarrollo rápido de interfaces gráficas en Python utilizando la librería estándar **Tkinter**. Su filosofía se basa en el desacoplamiento: diseña visualmente, exporta a JSON y controla la lógica desde Python sin ensuciar tu código con coordenadas.

---

## 🚀 Características Principales

- **Desacoplamiento UI/Logic:** Define tu interfaz en archivos `.tkd` (JSON) y mantén tu código Python limpio.
- **Zero Dependencies:** El loader utiliza únicamente la librería estándar de Python. No requiere paquetes pesados.
- **Absolute Positioning:** Control total sobre la ubicación y tamaño de los widgets.
- **Extensible:** Fácil acceso a los objetos nativos de Tkinter para personalizaciones avanzadas.

---

# 📖 Guía de Uso

## 1. El archivo de diseño (.tkd)
El loader interpreta un esquema JSON que define los componentes de la interfaz:

```json
[
    {
        "id": "main_button",
        "type": "TButton",
        "x": 100,
        "y": 150,
        "width": 120,
        "height": 40,
        "text": "Enviar Datos"
    }
]
```

## 2. Implementación en Python

```python
import tkinter as tk
from tk_designer import TKDLoader

def handle_click():
    print("¡Acción ejecutada desde el controlador!")

# Configuración básica
root = tk.Tk()
root.geometry("800x600")

# Inicialización del Loader
app = TKDLoader(root, "mainwindow.tkd")

# Conexión de Slots (Eventos)
app.connect("main_button", handle_click)

root.mainloop()
```

# 🔧 API Reference
  | Método | Descripción |
|--------|-------------|
| `TKDLoader(master, file_path)` | Clase principal que renderiza la interfaz. |
| `.connect(widget_id, function, event="<Button-1>")` | Enlaza un widget a una función de Python. |
| `.get_value(widget_id)` | Método de conveniencia para obtener el contenido de widgets de entrada (como Entry). |
| `.widgets` | Diccionario que contiene las instancias reales de los widgets de Tkinter. |


