# lector_archivos.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from werkzeug.datastructures import FileStorage # Tipo de dato de archivos de Flask
import pandas as pd # <-- ¡Necesario para las implementaciones concretas!

# 1. INTERFAZ (Contrato) - ILectorDeArchivos
class ILectorDeArchivos(ABC):
    """Interfaz para cualquier clase que lea archivos de inventario."""
    
    @abstractmethod
    def leer_datos(self, archivo: FileStorage) -> List[Dict[str, Any]]:
        """
        Contrato: Recibe el objeto FileStorage subido por Flask y 
        retorna los datos del archivo en formato Lista de Diccionarios.
        """
        pass

# 2. IMPLEMENTACIÓN CONCRETA 1: Lector CSV
class LectorCSV(ILectorDeArchivos):
    def leer_datos(self, archivo: FileStorage) -> List[Dict[str, Any]]:
        # Pandas lee directamente el archivo subido
        df = pd.read_csv(archivo.stream)
        # Convertimos el DataFrame a Lista de Diccionarios
        return df.to_dict(orient='records')

# 3. IMPLEMENTACIÓN CONCRETA 2: Lector Excel
class LectorExcel(ILectorDeArchivos):
    def leer_datos(self, archivo: FileStorage) -> List[Dict[str, Any]]:
        # Pandas lee directamente el archivo subido
        # Es crucial usar 'engine=openpyxl'
        df = pd.read_excel(archivo.stream, engine='openpyxl') 
        # Convertimos el DataFrame a Lista de Diccionarios
        return df.to_dict(orient='records')