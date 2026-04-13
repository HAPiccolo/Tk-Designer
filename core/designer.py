class DesignerCore:
    """Gestiona el estado lógico del diseño actual."""

    def __init__(self):
        self.components = []  # Lista de widgets activos en el canvas
        self.selected_component = None

    def add_component(self, widget_instance):
        self.components.append(widget_instance)

    def remove_component(self, widget_instance):
        if widget_instance in self.components:
            self.components.remove(widget_instance)
            widget_instance.destroy()

    def get_all_data(self):
        """Serializa todos los componentes para el parser."""
        data = []
        for w in self.components:
            if hasattr(w, "id_name"):
                info = {
                    "id": w.id_name,
                    "type": w.winfo_class(),
                    "x": w.winfo_x(),
                    "y": w.winfo_y(),
                    "width": w.winfo_width(),
                    "height": w.winfo_height(),
                }
                # Intentar extraer propiedades dinámicamente
                for prop in ["text", "bg", "fg"]:
                    try:
                        info[prop] = w.cget(prop)
                    except:
                        pass
                data.append(info)
        return data
