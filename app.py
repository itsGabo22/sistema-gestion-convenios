# app.py

from flask import Flask, render_template, redirect, url_for, request
from modelos import analizar_convenio, cargar_convenios_desde_csv
from datetime import date
import csv

# Inicializa la aplicación Flask
app = Flask(__name__)

CSV_FILE = 'convenios.csv'

def guardar_convenios_en_csv(convenios):
    """
    Escribe la lista completa de convenios de vuelta al archivo CSV.
    """
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as archivo:
        # Usamos los campos de la dataclass Convenio como cabeceras
        cabeceras = convenios[0].__dataclass_fields__.keys() if convenios else []
        escritor = csv.DictWriter(archivo, fieldnames=cabeceras)
        escritor.writeheader()
        escritor.writerows([c.__dict__ for c in convenios])

@app.route('/') # Define la ruta principal de la web
def dashboard_convenios():
    """
    Carga los convenios, los analiza y los muestra en una plantilla HTML.
    """
    # 1. Obtener el término de búsqueda desde los argumentos de la URL (?q=...)
    search_query = request.args.get('q', '')

    # 1. Cargar los convenios desde el CSV
    convenios = cargar_convenios_desde_csv(CSV_FILE)

    # 2. Si hay un término de búsqueda, filtrar la lista de convenios
    if search_query:
        convenios = [
            c for c in convenios 
            if search_query.lower() in c.nombre.lower() or search_query.lower() in c.entidad.lower()
        ]
    
    # 3. Analizar cada convenio (ya filtrado) para obtener su estado y días restantes
    convenios_analizados = [(convenio, analizar_convenio(convenio.fecha_vencimiento)) for convenio in convenios]
    
    # 4. Renderizar la plantilla HTML, pasándole los datos y el término de búsqueda
    return render_template('index.html', convenios=convenios_analizados, search_query=search_query)

@app.route('/eliminar/<int:convenio_id>')
def eliminar_convenio(convenio_id):
    """
    Elimina un convenio por su ID y guarda los cambios en el CSV.
    """
    convenios = cargar_convenios_desde_csv(CSV_FILE)
    convenios_filtrados = [c for c in convenios if c.id != convenio_id]
    
    if len(convenios_filtrados) < len(convenios):
        guardar_convenios_en_csv(convenios_filtrados)

    return redirect(url_for('dashboard_convenios'))

@app.route('/renovar/<int:convenio_id>')
def renovar_convenio(convenio_id):
    """
    Renueva un convenio (añade 1 año a su fecha de vencimiento) y guarda los cambios.
    """
    convenios = cargar_convenios_desde_csv(CSV_FILE)
    for convenio in convenios:
        if convenio.id == convenio_id:
            # Añade 365 días a la fecha de vencimiento actual
            convenio.fecha_vencimiento = convenio.fecha_vencimiento.replace(year=convenio.fecha_vencimiento.year + 1)
            break
    
    guardar_convenios_en_csv(convenios)
    return redirect(url_for('dashboard_convenios'))

if __name__ == '__main__':
    app.run(debug=True) # Inicia el servidor en modo de depuración