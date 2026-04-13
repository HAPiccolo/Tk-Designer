import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Importaciones de tu estructura modular
from core.designer import DesignerCore
from core.parser import TKDParser
from ui.toolbox import ToolboxPanel
from ui.workspace import WorkspaceCanvas
from ui.properties import PropertiesPanel
from ui.widget_tree import WidgetTreePanel
from widgets.base import DraggableWidget


class TKDesigner(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE ESTILO ---
        style = ttk.Style()
        style.theme_use("clam")

        # Paleta de colores VSCode/Carbon
        bg_dark = "#1e1e1e"
        bg_panel = "#252526"
        accent_blue = "#007acc"
        fg_white = "#ffffff"
        fg_gray = "#cccccc"

        # Configuración General
        style.configure(
            ".", background=bg_dark, foreground=fg_white, font=("Segoe UI", 10)
        )

        # Paneles y PanedWindow
        style.configure("TPanedwindow", background="#121212")
        style.configure("TFrame", background=bg_panel)

        # Entradas de Texto (Entry)
        style.configure(
            "TEntry",
            fieldbackground="#3c3c3c",
            foreground="white",
            insertcolor="white",
            borderwidth=0,
        )

        # Etiquetas (Labels)
        style.configure("TLabel", background=bg_panel, foreground=fg_white)
        style.configure(
            "Editor.TLabel",
            background=bg_panel,
            foreground=accent_blue,
            font=("Segoe UI", 9, "bold"),
        )

        # Botones de la Toolbox (Cuadrícula)
        style.configure(
            "Toolbox.TButton",
            font=("Segoe UI", 8),
            padding=5,
            width=8,
            background="#2d2d2d",
            foreground="white",
        )
        style.map("Toolbox.TButton", background=[("active", accent_blue)])

        # Botones Generales (Guardar/Eliminar)
        style.configure("TButton", padding=5, background="#333333", foreground="white")
        style.map("TButton", background=[("active", accent_blue)])

        # Scrollbar (Fina y oscura)
        style.configure(
            "Vertical.TScrollbar",
            arrowsize=14,
            background="#333333",
            troughcolor=bg_dark,
            bordercolor=bg_dark,
            relief="flat",
        )

        # Árbol de Jerarquía (Treeview)
        style.configure(
            "Treeview",
            background=bg_dark,
            foreground=fg_gray,
            fieldbackground=bg_dark,
            borderwidth=0,
            rowheight=24,
        )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#004b82")],
            foreground=[("selected", "white")],
        )

        # Labelframe (Contenedor de Jerarquía)
        style.configure(
            "TLabelframe",
            background=bg_panel,
            foreground=accent_blue,
            bordercolor="#333333",
        )
        style.configure(
            "TLabelframe.Label",
            background=bg_panel,
            foreground=accent_blue,
            font=("Segoe UI", 9, "bold"),
        )

        # Configuración de Ventana
        self.title("TK-Designer Professional v1.0")
        self.geometry("12800x800")
        self.configure(bg=bg_dark)

        # Inicializar lógica y UI
        self.designer_logic = DesignerCore()
        self._create_menu()
        self._setup_layout()

    def _setup_layout(self):
        """Organiza los paneles con un diseño equilibrado."""
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill="both", expand=True)

        # --- PANEL IZQUIERDO ---
        self.left_panel = ttk.Frame(self.paned)

        # Toolbox (Se expande para ocupar el espacio superior)
        self.toolbox = ToolboxPanel(self.left_panel, spawn_callback=self.spawn)
        self.toolbox.pack(fill="both", expand=True, side="top", padx=5, pady=5)

        # Jerarquía (Fija abajo con altura controlada en su clase)
        self.widget_tree = WidgetTreePanel(
            self.left_panel, select_callback=self.on_widget_selected
        )
        self.widget_tree.pack(fill="x", side="bottom", padx=5, pady=(0, 10))

        # --- PANEL CENTRAL ---
        self.workspace = WorkspaceCanvas(self.paned)

        # --- PANEL DERECHO ---
        self.props = PropertiesPanel(self.paned, padding=10)

        # Registro en PanedWindow
        self.paned.add(self.left_panel, weight=1)
        self.paned.add(self.workspace, weight=4)
        self.paned.add(self.props, weight=1)

    def _create_menu(self):
        """Menú superior integrado al estilo oscuro manual."""
        m_bg, m_fg = "#2d2d2d", "#cccccc"
        m_sel = "#3e3e42"

        self.menu_bar = tk.Menu(self, bg=m_bg, fg=m_fg, activebackground=m_sel, bd=0)

        file_menu = tk.Menu(
            self.menu_bar, tearoff=0, bg=m_bg, fg=m_fg, activebackground=m_sel, bd=0
        )
        file_menu.add_command(label="Nuevo Proyecto", command=self.reset_workspace)
        file_menu.add_command(
            label="Exportar diseño (.tkd)", command=self.export_design
        )
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)

        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        self.config(menu=self.menu_bar)

    def spawn(self, cls):
        """Instancia un nuevo widget y lo registra."""
        new_w = cls(self.workspace)

        # Asignar ID automático
        count = len(self.designer_logic.components) + 1
        new_w.id_name = f"{cls.__name__.lower()}_{count}"

        # Config inicial por clase
        if cls == ttk.Progressbar:
            new_w.config(value=50, length=100)
        elif cls == tk.Text:
            new_w.config(width=20, height=5)
        elif cls == tk.Frame:
            new_w.config(bg="#d1d1d1", width=100, height=100)
        elif "text" in new_w.keys():
            new_w.config(text=f"Nuevo {cls.__name__}")

        new_w.place(x=100, y=100)

        # Lógica de arrastre y selección
        DraggableWidget(new_w, self.workspace, self.on_widget_selected)
        self.designer_logic.add_component(new_w)

        # Actualizar UI
        self.on_widget_selected(new_w)
        self.widget_tree.update_tree(self.designer_logic.components)

    def on_widget_selected(self, widget):
        """Sincroniza el foco visual y los paneles laterales."""
        for child in self.workspace.winfo_children():
            try:
                if child != self.workspace.grid_canvas:
                    child.config(highlightthickness=0)
            except:
                pass

        try:
            widget.config(highlightthickness=2, highlightbackground="#3498db")
            widget.focus_set()
        except:
            pass

        self.props.load_widget(widget)

    def reset_workspace(self):
        if messagebox.askyesno("Nuevo Proyecto", "¿Desea borrar el diseño actual?"):
            self.workspace.clear()
            self.designer_logic.components = []
            self.widget_tree.update_tree([])

    def export_design(self):
        data = self.designer_logic.get_all_data()
        if not data:
            messagebox.showwarning("Exportar", "El área de trabajo está vacía.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".tkd", filetypes=[("TKD Files", "*.tkd")]
        )
        if path and TKDParser.save_to_file(path, data):
            messagebox.showinfo("Éxito", "Diseño exportado correctamente.")


if __name__ == "__main__":
    app = TKDesigner()
    app.mainloop()
