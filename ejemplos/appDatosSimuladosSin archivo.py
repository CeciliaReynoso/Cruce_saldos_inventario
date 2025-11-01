# app.py (Código para la ruta /procesar)

from flask import Flask
from exportador import ExportadorCSV, ExportadorExcel # Importación de la implementación concreta
from inventario_servicio import ServicioDeInventario

app = Flask(__name__)

# Definimos una ruta simple para probar, usando POST como si viniera de un formulario
@app.route("/procesar", methods=["POST", "GET"]) 
def procesar_inventario_web():
    
    # --- SIMULACIÓN DE DATOS (En el futuro, aquí leerás los archivos subidos) ---
    datos_maestro = [
        {'sku': 'A100', 'cantidad': 100},
        {'sku': 'B200', 'cantidad': 50},
        {'sku': 'C300', 'cantidad': 10} # Este SKU tiene 10 y nadie lo contó (diferencia -10)
    ]
    datos_conteo = [
        {'sku': 'A100', 'cantidad': 95}, # Diferencia: -5
        {'sku': 'B200', 'cantidad': 50}, # Diferencia: 0 (No debe aparecer en el resultado)
        {'sku': 'D400', 'cantidad': 5},  # Diferencia: +5 (Estaba en conteo, no en maestro)
    ]
    
    # 1. COMPOSICIÓN (Inyección de Dependencia)
    exportador_concreto = ExportadorExcel() 
    servicio = ServicioDeInventario(exportador=exportador_concreto)

    # 2. EJECUCIÓN DEL SERVICIO
    # Llama al método que cruza la lógica y luego llama a la exportación
    resultado_proceso = servicio.procesar_inventario(datos_maestro, datos_conteo)
    
    # 3. RETORNO A LA WEB
    # Flask muestra esta cadena de texto en el navegador
    return resultado_proceso 


# Mantenemos la ruta home para saber que el servidor está corriendo
@app.route("/")
def home():
    return "¡Inventario en línea! Usa la ruta /procesar para ejecutar la lógica."