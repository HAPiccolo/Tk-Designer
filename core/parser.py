import json
import os


class TKDParser:
    """Módulo encargado de la persistencia de datos (E/S)."""

    @staticmethod
    def save_to_file(file_path, data):
        """Guarda la lista de widgets en un archivo JSON con extensión .tkd"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def load_from_file(file_path):
        """Lee el archivo .tkd y devuelve una lista de diccionarios."""
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar: {e}")
            return []
