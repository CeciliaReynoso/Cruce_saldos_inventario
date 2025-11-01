# exportador.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any
# Importamos Pandas (librería para manejo de datos)
import pandas as pd

# 1. INTERFAZ (Abstracción) - IExportadorDeDatos
class IExportadorDeDatos(ABC):
    """Interfaz para cualquier clase que exporte datos de inventario."""
    
    @abstractmethod
    def guardar_resultados(self, datos: List[Dict[str, Any]]) -> str:
        """
        Contrato: Recibe una lista de diccionarios (datos) y debe retornar
        una cadena de texto con la ruta del archivo creado.
        """
        pass

# 2. IMPLEMENTACIÓN CONCRETA 1: Exportador CSV
class ExportadorCSV(IExportadorDeDatos):
    def guardar_resultados(self, datos: List[Dict[str, Any]]) -> str:
        """Guarda la lista de diccionarios como un archivo CSV real."""
        
        df = pd.DataFrame(datos)
        archivo_salida = f"reporte_diferencias_{len(df)}.csv"
        
        # GUARDADO REAL de CSV
        df.to_csv(archivo_salida, index=False)
        
        return f"Archivo guardado: {archivo_salida}"

# 3. IMPLEMENTACIÓN CONCRETA 2: Exportador Excel (¡NUEVA IMPLEMENTACIÓN REAL!)
# Cumple LSP. Puede sustituir a CSV sin romper el servicio.
class ExportadorExcel(IExportadorDeDatos):
    def guardar_resultados(self, datos: List[Dict[str, Any]]) -> str:
        """Guarda la lista de diccionarios como un archivo Excel (XLSX) real."""
        
        df = pd.DataFrame(datos)
        archivo_salida = f"reporte_diferencias_{len(df)}.xlsx"
        
        # GUARDADO REAL de Excel
        # Usa el motor 'openpyxl' (por eso lo instalamos)
        df.to_excel(archivo_salida, index=False, engine='openpyxl')
        
        return f"Archivo guardado: {archivo_salida}"