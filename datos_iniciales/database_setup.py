# database_setup.py

import sqlite3
import csv

DATABASE_FILE = 'database.db'

def create_database():
    """
    Crea la base de datos y las tablas necesarias si no existen.
    """
    print("Creando la base de datos y las tablas...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Crear la tabla de convenios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS convenios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            entidad TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            responsable TEXT,
            tipo TEXT,
            renovaciones INTEGER,
            horas_practica INTEGER,
            evaluacion_empresa TEXT,
            beneficios TEXT
        )
    ''')

    # Crear la tabla de evaluaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_convenio INTEGER NOT NULL,
            nombre_estudiante TEXT NOT NULL,
            calificacion INTEGER,
            comentarios TEXT,
            FOREIGN KEY (id_convenio) REFERENCES convenios (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Tablas creadas con éxito.")

def import_data_from_csv():
    """
    Importa los datos de los archivos CSV a las tablas de la base de datos.
    """
    print("Importando datos desde los archivos CSV...")
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Importar convenios.csv
    with open('convenios.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO convenios (id, nombre, entidad, fecha_vencimiento, responsable, tipo, renovaciones, horas_practica, evaluacion_empresa, beneficios)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row.values()))

    # Importar evaluaciones.csv
    with open('evaluaciones.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO evaluaciones (id_convenio, nombre_estudiante, calificacion, comentarios)
                VALUES (?, ?, ?, ?)
            ''', tuple(row.values()))

    conn.commit()
    conn.close()
    print("Datos importados con éxito.")

if __name__ == '__main__':
    create_database()
    import_data_from_csv()
    print("\n¡Configuración de la base de datos completada! Ya puedes ejecutar la aplicación principal.")