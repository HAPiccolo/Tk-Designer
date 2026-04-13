import tkinter as tk
from tkinter import ttk, colorchooser, messagebox


class PropertiesPanel(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Editor de Componente", **kwargs)
        self.current_widget = None
        self.prop_vars = {}
        self.id_var = tk.StringVar()

    def load_widget(self, widget):
        """Carga el widget y crea variables vinculadas a sus propiedades."""
        self.current_widget = widget

        for child in self.winfo_children():
            child.destroy()

        self.prop_vars = {}

        # --- 1. SECCIÓN ID ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(top_frame, text="ID (Variable):", font=("Arial", 9, "bold")).pack(
            anchor="w"
        )
        self.id_var.set(getattr(widget, "id_name", ""))
        ttk.Entry(top_frame, textvariable=self.id_var).pack(fill="x", pady=2)

        z_frame = ttk.Frame(top_frame)
        z_frame.pack(fill="x", pady=5)
        ttk.Button(z_frame, text="🔼 Frente", command=self.move_up).pack(
            side="left", expand=True, fill="x", padx=2
        )
        ttk.Button(z_frame, text="🔽 Fondo", command=self.move_down).pack(
            side="left", expand=True, fill="x", padx=2
        )

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)

        # --- 2. SECCIÓN ATRIBUTOS ---
        attr_frame = ttk.Frame(self)
        attr_frame.pack(fill="both", expand=True, padx=5)

        props = ["text", "width", "height", "bg", "fg"]

        for i, p in enumerate(props):
            try:
                current_val = str(widget.cget(p))
                var = tk.StringVar(value=current_val)
                self.prop_vars[p] = var

                ttk.Label(attr_frame, text=f"{p}:").grid(
                    row=i, column=0, sticky="w", pady=2
                )
                ent = ttk.Entry(attr_frame, textvariable=var)
                ent.grid(row=i, column=1, sticky="ew", padx=5, pady=2)

                if p in ["bg", "fg"]:
                    ttk.Button(
                        attr_frame,
                        text="🎨",
                        width=3,
                        command=lambda pr=p, v=var: self._pick_color(pr, v),
                    ).grid(row=i, column=2)
            except Exception:
                continue

        attr_frame.columnconfigure(1, weight=1)

        # --- 3. BOTONES DE ACCIÓN ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(btn_frame, text="✅ GUARDAR CAMBIOS", command=self.apply).pack(
            fill="x", padx=10, pady=2
        )
        ttk.Button(
            btn_frame, text="❌ ELIMINAR WIDGET", command=self.delete_current
        ).pack(fill="x", padx=10)

    def _pick_color(self, prop, var):
        color = colorchooser.askcolor(title=f"Elegir color para {prop}")
        if color[1]:
            var.set(color[1])
            self.apply()

    def apply(self):
        """Aplica los valores y refresca el Árbol en el main."""
        if not self.current_widget:
            return

        new_id = self.id_var.get().strip().replace(" ", "_")
        self.current_widget.id_name = new_id

        config_to_apply = {}
        for prop, var in self.prop_vars.items():
            value = var.get()
            if prop in ["width", "height"]:
                try:
                    value = int(value)
                except ValueError:
                    continue
            config_to_apply[prop] = value

        try:
            self.current_widget.config(**config_to_apply)

            # --- NOTIFICAR AL MAIN ---
            root = self.winfo_toplevel()
            if hasattr(root, "refresh_widget_tree"):
                root.refresh_widget_tree()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar:\n{e}")

    def move_up(self):
        if self.current_widget:
            self.current_widget.lift()

    def move_down(self):
        if self.current_widget:
            # Importante: usamos tk.Frame.lower para evitar el error de argumentos del canvas
            tk.Frame.lower(self.current_widget)

    def delete_current(self):
        """Elimina el widget de la pantalla, de la lógica y del árbol."""
        if self.current_widget:
            root = self.winfo_toplevel()

            # 1. Quitar de la lógica del Core
            if hasattr(root, "designer_logic"):
                root.designer_logic.remove_component(self.current_widget)

            # 2. Destruir físicamente
            self.current_widget.destroy()
            self.current_widget = None

            # 3. Limpiar panel de propiedades
            for child in self.winfo_children():
                child.destroy()

            # 4. Refrescar el árbol de widgets
            if hasattr(root, "refresh_widget_tree"):
                root.refresh_widget_tree()
