import tkinter as tk
from tkinter import ttk
from core.registry import WIDGET_CATALOG


class ToolboxPanel(ttk.Frame):
    def __init__(self, master, spawn_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.spawn_callback = spawn_callback
        self._setup_ui()

    def _setup_ui(self):
        # Título
        label = ttk.Label(
            self,
            text="Herramientas",
            font=("Segoe UI", 10, "bold"),
            foreground="#007acc",
        )
        label.pack(pady=(5, 10), anchor="w", padx=10)

        # Contenedor principal sin bordes extraños
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Canvas para scroll (solo vertical si fuera necesario)
        self.canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Grilla de botones (2 columnas compactas)
        row, col = 0, 0
        for name, info in WIDGET_CATALOG.items():
            icon = info.get("icon", "")
            btn = ttk.Button(
                self.scrollable_frame,
                text=f"{icon}\n{name}",
                width=9,  # Ancho exacto para 2 columnas
                command=lambda c=info["class"]: self.spawn_callback(c),
                style="Toolbox.TButton",
            )
            btn.grid(row=row, column=col, padx=4, pady=4)

            col += 1
            if col > 1:
                col = 0
                row += 1
