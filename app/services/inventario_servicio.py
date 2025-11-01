# inventario_servicio.py

from typing import List, Dict, Any
# Importamos la interfaz para cumplir con el DIP
from exportador import IExportadorDeDatos 

class ServicioDeInventario:
    
    # CONSTRUCTOR: Recibe la dependencia (IExportadorDeDatos)
    def __init__(self, exportador: IExportadorDeDatos):
        # Almacenamos la referencia del exportador inyectado
        self.exportador = exportador 
        
    def procesar_inventario(self, datos_maestro: List[Dict], datos_conteo: List[Dict]) -> str:
        """
        Método principal que orquesta el cruce y la exportación de resultados.
        """
        # 1. Ejecutar Lógica de Negocio Pura (Lógica de cruce corregida)
        diferencias = self._calcular_diferencias(datos_maestro, datos_conteo)
        
        # 2. Uso de la Abstracción (Exportación)
        # Llama a 'guardar_resultados' sin saber si es CSV o Excel (DIP, LSP)
        ruta_archivo = self.exportador.guardar_resultados(diferencias)
        
        return f"Proceso completado. Archivo de diferencias listo: {ruta_archivo}"
    
    # MÉTODO PRIVADO: Contiene la lógica de cruce (CORREGIDA)
    def _calcular_diferencias(self, datos_maestro: List[Dict], datos_conteo: List[Dict]) -> List[Dict]:
        """
        Cruza los datos buscando todos los SKUs ÚNICOS en ambos conjuntos
        para asegurar que se capturen faltantes y sobrantes.
        """
        diferencias_finales = []
        
        # 1. TRASLADAR AMBOS A DICCIONARIOS PARA BÚSQUEDA RÁPIDA (Full Join)
        maestro_por_sku = {item['sku']: item['cantidad'] for item in datos_maestro}
        conteo_por_sku = {item['sku']: item['cantidad'] for item in datos_conteo}
        
        # 2. IDENTIFICAR TODOS LOS SKUS ÚNICOS (Unión de claves)
        # Esto asegura que procesemos: [A100, B200, C300, D400]
        todos_los_skus = set(maestro_por_sku.keys()) | set(conteo_por_sku.keys())

        # 3. PROCESAR CADA SKU ÚNICO
        for sku_actual in todos_los_skus:
            
            # Obtener cantidades (usa 0 si el SKU no existe en ese diccionario)
            cantidad_maestra = maestro_por_sku.get(sku_actual, 0)
            cantidad_conteo = conteo_por_sku.get(sku_actual, 0)
            
            # 4. CALCULAR LA DIFERENCIA
            diferencia = cantidad_conteo - cantidad_maestra
            
            # 5. FILTRAR POR LA REGLA DE NEGOCIO (Diferencia != 0)
            if diferencia != 0:
                diferencia_de_fila = {
                    'sku': sku_actual,
                    'conteo_maestro': cantidad_maestra,
                    'conteo_fisico': cantidad_conteo,
                    'diferencia': diferencia,
                }
                diferencias_finales.append(diferencia_de_fila)
        
        return diferencias_finales