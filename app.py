# app.py

from flask import Flask, request, render_template, redirect, url_for, send_file, flash, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'services'))

from exportador import ExportadorCSV, ExportadorExcel 
from inventario_servicio import ServicioDeInventario
# Importamos ambas implementaciones del Lector para la inyección (DIP/OCP)
from lector_archivos import LectorCSV, LectorExcel
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__, 
           template_folder='app/templates',
           static_folder='app/static')
app.secret_key = 'tu_clave_secreta_aqui_cambiala_en_produccion'  # Cambia esto en producción

# Configuración de la aplicación
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB máximo
UPLOAD_FOLDER = 'data/temp'
RESULTS_FOLDER = 'data/temp'

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# --- FUNCIÓN DE AYUDA: OBTENER EXTENSIÓN ---
def obtener_extension(filename):
    """Extrae la extensión del nombre de archivo."""
    if '.' in filename:
        return filename.rsplit('.', 1)[-1].lower()
    return ''
# --------------------------------------------

@app.route("/")
def home():
    # Muestra el formulario HTML que creamos
    return render_template("upload.html") 

@app.route("/procesar", methods=["POST", "GET"]) 
def procesar_inventario_web():
    
    if request.method == 'POST':
        try:
            # 1. OBTENER ARCHIVOS Y OPCIONES DEL FORMULARIO
            archivo_maestro = request.files.get('maestro')
            archivo_conteo = request.files.get('conteo')
            formato_salida = request.form.get('formato_salida', 'CSV')

            if not archivo_maestro or not archivo_conteo:
                flash("Error: Por favor, suba ambos archivos.", "error")
                return redirect(url_for('home'))
            
            # Validar nombres de archivos
            if archivo_maestro.filename == '' or archivo_conteo.filename == '':
                flash("Error: Por favor, seleccione archivos válidos.", "error")
                return redirect(url_for('home'))
            
            # 2. INYECCIÓN DEL LECTOR
            extension = obtener_extension(archivo_maestro.filename)

            if extension == 'csv':
                lector_concreto = LectorCSV()
            elif extension in ('xlsx', 'xls'):
                lector_concreto = LectorExcel()
            else:
                flash("Error: Formato de archivo no soportado (solo CSV o XLSX).", "error")
                return redirect(url_for('home'))

            # 3. PROCESAMIENTO
            datos_maestro = lector_concreto.leer_datos(archivo_maestro)
            datos_conteo = lector_concreto.leer_datos(archivo_conteo)
            
            # Calcular estadísticas antes del procesamiento
            stats = {
                'items_maestro': len(datos_maestro),
                'items_conteo': len(datos_conteo)
            }

            # 4. INYECCIÓN DEL EXPORTADOR
            if formato_salida == 'Excel':
                exportador_concreto = ExportadorExcel()
            else:
                exportador_concreto = ExportadorCSV()
                
            servicio = ServicioDeInventario(exportador=exportador_concreto)
            
            # 5. EJECUCIÓN DEL SERVICIO
            resultado_proceso = servicio.procesar_inventario(datos_maestro, datos_conteo)
            
            # Extraer nombre del archivo del resultado
            nombre_archivo = extraer_nombre_archivo(resultado_proceso)
            
            # Calcular diferencias para estadísticas
            stats['diferencias'] = calcular_numero_diferencias(nombre_archivo)
            
            # 6. RENDERIZAR PÁGINA DE RESULTADO
            return render_template('resultado.html', 
                                 mensaje=resultado_proceso,
                                 nombre_archivo=nombre_archivo,
                                 stats=stats)
            
        except Exception as e:
            flash(f"Error al procesar los archivos: {str(e)}", "error")
            return redirect(url_for('home'))

    # Si se accede por GET sin subir archivos, redirige al formulario
    return redirect(url_for('home'))

@app.route("/descargar/<filename>")
def descargar_archivo(filename):
    """Ruta para descargar archivos de resultado"""
    try:
        # Verificar que el archivo existe y está en el directorio permitido
        ruta_archivo = os.path.join(os.getcwd(), filename)
        
        if not os.path.exists(ruta_archivo):
            flash("El archivo solicitado no existe o ha expirado.", "error")
            return redirect(url_for('home'))
            
        return send_file(ruta_archivo, as_attachment=True)
    except Exception as e:
        flash(f"Error al descargar el archivo: {str(e)}", "error")
        return redirect(url_for('home'))

@app.route("/api/preview/<filename>")
def vista_previa_api(filename):
    """API para obtener vista previa del archivo de resultados"""
    try:
        ruta_archivo = os.path.join(os.getcwd(), filename)
        
        if not os.path.exists(ruta_archivo):
            return jsonify({'error': 'Archivo no encontrado'}), 404
            
        # Leer las primeras filas del archivo
        if filename.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        else:
            df = pd.read_excel(ruta_archivo)
            
        # Tomar solo las primeras 10 filas
        preview_data = df.head(10).to_dict('records')
        
        return jsonify({
            'data': preview_data,
            'total_rows': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/ejemplos/<filename>")
def descargar_ejemplo(filename):
    """Ruta para descargar archivos de ejemplo"""
    try:
        archivos_permitidos = ['inventario_maestro_demo.csv', 'conteo_fisico_demo.csv']
        
        if filename not in archivos_permitidos:
            flash("Archivo de ejemplo no encontrado.", "error")
            return redirect(url_for('home'))
            
        ruta_archivo = os.path.join(os.getcwd(), 'data', 'samples', filename)
        
        if not os.path.exists(ruta_archivo):
            flash("Archivo de ejemplo no disponible.", "error")
            return redirect(url_for('home'))
            
        return send_file(ruta_archivo, as_attachment=True)
        
    except Exception as e:
        flash(f"Error al descargar archivo de ejemplo: {str(e)}", "error")
        return redirect(url_for('home'))

# --- FUNCIONES AUXILIARES ---
def extraer_nombre_archivo(mensaje):
    """Extrae el nombre del archivo del mensaje de resultado"""
    try:
        # Busca el patrón "reporte_diferencias_X.csv" o "reporte_diferencias_X.xlsx" en el mensaje
        import re
        patron = r'(reporte_diferencias_\d+\.\w+)'
        match = re.search(patron, mensaje)
        if match:
            return match.group(1)
    except:
        pass
    return None

def calcular_numero_diferencias(nombre_archivo):
    """Calcula el número de diferencias en el archivo generado"""
    if not nombre_archivo:
        return 0
        
    try:
        ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
        if os.path.exists(ruta_archivo):
            if nombre_archivo.endswith('.csv'):
                df = pd.read_csv(ruta_archivo)
            else:
                df = pd.read_excel(ruta_archivo)
            return len(df)
    except:
        pass
    return 0

def archivo_permitido(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    EXTENSIONES_PERMITIDAS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

# --- MANEJADORES DE ERROR ---
@app.errorhandler(413)
def archivo_muy_grande(error):
    flash("El archivo es demasiado grande. Tamaño máximo permitido: 10MB", "error")
    return redirect(url_for('home'))

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_servidor(error):
    flash("Ha ocurrido un error interno del servidor. Por favor, intente nuevamente.", "error")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)