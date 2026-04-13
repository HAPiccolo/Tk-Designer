import tkinter as tk
from tkd_loader import TKDLoader

# --- FUNCIONES ---


def procesar_datos():
    # Usamos el ID 'entry_2' que definiste en tu JSON
    contenido = gui.get_value("entry_2")

    if contenido.strip() == "":
        print("⚠️ El campo está vacío. Escribí algo antes de presionar el botón.")
        # Ejemplo: Cambiar color de fondo del entry si está vacío
        gui.widgets["entry_2"].config(bg="#ffcccc")
    else:
        print(f"✅ Botón presionado. Enviando: {contenido}")
        # Resetear color si escribió algo
        gui.widgets["entry_2"].config(bg="white")


# --- CONFIGURACIÓN DE LA VENTANA ---

root = tk.Tk()
root.title("tk-Designer test")
root.geometry("800x600")
root.configure(bg="#212121")  # Fondo oscuro para que resalte el diseño

# --- CARGA DEL DISEÑO ---

# Instanciamos el loader y le pasamos el archivo .tkd
gui = TKDLoader(root, "mainwindow.tkd")

# --- EDICIÓN DE SLOTS (CONEXIÓN) ---

# Conectamos el botón 'button_1' a nuestra función de Python
# No hace falta usar lambda si la función no recibe argumentos
gui.connect("button_1", procesar_datos)


root.mainloop()
