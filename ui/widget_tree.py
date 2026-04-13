import tkinter as tk
from tkinter import ttk


class WidgetTreePanel(ttk.LabelFrame):
    def __init__(self, master, select_callback, **kwargs):
        super().__init__(master, text="Jerarquía de Widgets", **kwargs)
        self.select_callback = select_callback

        # Configuración del Treeview: height=5 es el punto justo
        self.tree = ttk.Treeview(
            self, columns=("ID", "Tipo"), show="headings", height=5, selectmode="browse"
        )
        self.tree.heading("ID", text="ID / Variable")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.column("ID", width=110, anchor="w")
        self.tree.column("Tipo", width=70, anchor="c")

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.nodes = {}

    def update_tree(self, components):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.nodes = {}

        for widget in components:
            w_id = getattr(widget, "id_name", "N/A")
            w_type = widget.winfo_class().replace(
                "T", ""
            )  # Limpia el nombre (TButton -> Button)
            node_id = self.tree.insert("", "end", values=(w_id, w_type))
            self.nodes[node_id] = widget

    def _on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            widget = self.nodes.get(selected_item[0])
            if widget:
                self.select_callback(widget)
