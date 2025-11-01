from flask import Flask

# Crea la instancia de la aplicación
app = Flask(__name__)

# Define el decorador para la ruta principal (/)
@app.route("/")
def home():
    # Retorna la cadena de texto que se verá en el navegador
    return "¡Inventario en línea!"

