import tkinter as tk


class WorkspaceCanvas(tk.Frame):
    """
    El lienzo principal de diseño.
    Aquí es donde se posicionan y mueven los componentes.
    """

    def __init__(self, master, **kwargs):
        # Configuraciones por defecto para el canvas
        kwargs.setdefault("bg", "#ffffff")
        kwargs.setdefault("highlightthickness", 1)
        kwargs.setdefault("highlightbackground", "#cccccc")
        super().__init__(master, **kwargs)

        # Creamos el canvas para la cuadrícula
        self.grid_canvas = tk.Canvas(self, bg=kwargs["bg"], highlightthickness=0)
        self.grid_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # SOLUCIÓN AL ERROR: Especificamos que use el método lower de la clase base
        # para evitar la confusión con canvas.tag_lower
        tk.Frame.lower(self.grid_canvas)

        self.bind("<Configure>", self._draw_grid)

    def _draw_grid(self, event=None):
        """Dibuja puntos de guía sutiles."""
        self.grid_canvas.delete("grid")
        w = self.winfo_width()
        h = self.winfo_height()
        step = 20  # Espaciado de la cuadrícula

        for x in range(0, w, step):
            for y in range(0, h, step):
                # Dibujamos puntos sutiles para no molestar a la vista
                self.grid_canvas.create_oval(
                    x, y, x + 1, y + 1, fill="#e0e0e0", outline="#e0e0e0", tags="grid"
                )

    def clear(self):
        """Elimina todos los widgets del área de trabajo excepto la grilla."""
        for widget in self.winfo_children():
            if widget != self.grid_canvas:
                widget.destroy()
