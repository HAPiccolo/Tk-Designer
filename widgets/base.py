# widgets/base.py
import tkinter as tk


class DraggableWidget:
    def __init__(self, widget, workspace, select_callback):
        self.widget = widget
        self.workspace = workspace
        self.select_callback = select_callback
        self.grid_size = 20  # Debe coincidir con el step de workspace.py

        self.widget.bind("<Button-1>", self.on_start)
        self.widget.bind("<B1-Motion>", self.on_drag)

    def on_start(self, event):
        self._drag_data = {"x": event.x, "y": event.y}
        self.select_callback(self.widget)

    def on_drag(self, event):
        # Calcular cuánto se movió el ratón
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]

        # Calcular nueva posición teórica
        new_x = self.widget.winfo_x() + deltax
        new_y = self.widget.winfo_y() + deltay

        # --- LÓGICA DE SNAP TO GRID ---
        # Redondeamos al múltiplo de grid_size más cercano
        snap_x = (new_x // self.grid_size) * self.grid_size
        snap_y = (new_y // self.grid_size) * self.grid_size

        # Aplicar posición ajustada
        self.widget.place(x=snap_x, y=snap_y)

    def delete_me(self, event=None):
        self.widget.destroy()
