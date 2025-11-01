# inventario_servicio.py

from typing import List, Dict, Any
# Importamos la interfaz (la abstracción), NO las clases concretas (CSV/Excel)
from exportador import IExportadorDeDatos

# 1. El Servicio de alto nivel (Lógica de Negocio)
class ServicioDeInventario:
    
    # CONSTRUCTOR: Recibimos la dependencia (el Exportador) como un argumento.
    # El Servicio solo sabe que necesita un objeto que cumpla el contrato de la interfaz.
    def __init__(self, exportador: IExportadorDeDatos):
        self.exportador = exportador # Guardamos la referencia
        
    def procesar_inventario(self, datos_maestro: List[Dict], datos_conteo: List[Dict]) -> str:
        """Aquí va toda la lógica de cruce de datos y cálculo de diferencias."""
        
        # --- LÓGICA DE NEGOCIO PURA (NO TOCA ARCHIVOS) ---
        diferencias = self._calcular_diferencias(datos_maestro, datos_conteo)
        
        # --- USO DE LA ABSTRACCIÓN (DIP) ---
        # Llamamos al método guardar_resultados() del objeto que nos inyectaron.
        # NO sabemos si es CSV o Excel, y no nos importa.
        ruta_archivo = self.exportador.guardar_resultados(diferencias)
        
        return f"Proceso completado. Archivo de diferencias listo: {ruta_archivo}"

    def _calcular_diferencias(self, maestro, conteo) -> List[Dict]:
        # Implementación simple de ejemplo:
        # En la realidad, esto sería complejo (pandas, cruces, etc.)
        return [
            {'sku': 'AZ-452', 'diferencia': -5},
            {'sku': 'BX-100', 'diferencia': 2},
        ]