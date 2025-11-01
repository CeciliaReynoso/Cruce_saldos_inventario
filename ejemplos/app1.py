# app.py (El Coordinador / Composition Root)

from flask import Flask
# Importamos todas las piezas: la interfaz y las implementaciones
from exportador import ExportadorCSV
from inventario_servicio import ServicioDeInventario

app = Flask(__name__)

@app.route("/procesar", methods=["POST"]) # Crearemos una ruta para el procesamiento
def procesar_inventario_web():
    # 1. DECISIÓN Y COMPOSICIÓN (DI)
    # Creamos la implementación concreta de bajo nivel:
    exportador_concreto = ExportadorCSV() 

    # 2. INYECCIÓN
    # Creamos la instancia del Servicio (módulo de alto nivel) 
    # y le "inyectamos" la dependencia (el exportador) en su constructor:
    servicio = ServicioDeInventario(exportador=exportador_concreto)

    # Simulación de datos que vendrían del archivo subido:
    datos_maestro = [{'sku': 'A1', 'cantidad': 100}]
    datos_conteo = [{'sku': 'A1', 'cantidad': 95}]
    
    # 3. EJECUCIÓN DEL SERVICIO
    # Aquí vamos a llamar al método para que se ejecute la lógica de negocio.
    
    # ... tu código aquí ...

    # Por ahora, devolvemos un mensaje de éxito simple:
    return "Procesamiento iniciado. Revisa la terminal para ver el resultado."