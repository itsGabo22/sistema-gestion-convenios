# modelos.py

import sqlite3
import csv
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional

# 1. Estructura de datos para representar un convenio
@dataclass
class Convenio:
    """
    Representa un convenio institucional con sus datos principales.
    """
    id: int
    nombre: str
    entidad: str
    fecha_vencimiento: date
    responsable: str
    tipo: str
    renovaciones: int
    horas_practica: Optional[int] = None
    evaluacion_empresa: Optional[str] = None
    beneficios: Optional[str] = None

# Nueva estructura para las evaluaciones de estudiantes
@dataclass
class EvaluacionPractica:
    id_convenio: int
    nombre_estudiante: str
    calificacion: int
    comentarios: str

# Nueva estructura para el resultado del análisis
@dataclass
class AnalisisConvenio:
    """
    Contiene el resultado del análisis de estado de un convenio.
    """
    estado: 'EstadoConvenio'
    dias_restantes: int
    criticidad: int # El nuevo índice de criticidad

# 2. Enumeración para los estados del semáforo
class EstadoConvenio(Enum):
    """
    Define los posibles estados de un convenio según su fecha de vencimiento.
    """
    VERDE = "Verde"
    AMARILLO = "Amarillo"
    ROJO = "Rojo"

# 3. Lógica de negocio para determinar el estado
def analizar_convenio_ia(convenio: Convenio) -> AnalisisConvenio:
    """
    Calcula el estado de un convenio usando un modelo de puntuación de criticidad.
    """
    hoy = date.today()
    dias_restantes = (convenio.fecha_vencimiento - hoy).days
    
    # --- INICIO DEL MOTOR DE IA HEURÍSTICO ---
    
    # 1. Puntuación por Proximidad de Vencimiento
    if dias_restantes < 30:
        score_fecha = 50
    elif dias_restantes < 90:
        score_fecha = 30
    elif dias_restantes < 180:
        score_fecha = 10
    else:
        score_fecha = 0

    # 2. Puntuación por Tipo de Convenio (Importancia Estratégica)
    pesos_tipo = {'Practicas': 25, 'Movilidad': 20, 'Investigacion': 15, 'Academico': 10, 'Beneficio': 5}
    score_tipo = pesos_tipo.get(convenio.tipo, 0)

    # 3. Puntuación por Historial de Renovaciones
    score_renovaciones = min(convenio.renovaciones * 2, 10) # 2 puntos por renovación, con un máximo de 10

    # Cálculo del Índice de Criticidad Total
    indice_criticidad = score_fecha + score_tipo + score_renovaciones

    # --- FIN DEL MOTOR DE IA ---

    # El semáforo ahora se basa en el Índice de Criticidad
    estado_actual: EstadoConvenio
    if indice_criticidad > 50:
        estado_actual = EstadoConvenio.ROJO
    elif indice_criticidad > 25:
        estado_actual = EstadoConvenio.AMARILLO
    else:
        estado_actual = EstadoConvenio.VERDE
    
    return AnalisisConvenio(estado=estado_actual, dias_restantes=dias_restantes, criticidad=indice_criticidad)

def get_db_connection():
    """
    Establece una conexión con la base de datos y la configura para devolver filas tipo diccionario.
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def cargar_convenios_desde_db() -> list[Convenio]:
    """
    Carga todos los convenios desde la base de datos SQLite.
    """
    conn = get_db_connection()
    convenios_db = conn.execute('SELECT * FROM convenios').fetchall()
    conn.close()
    
    lista_convenios = []
    for row in convenios_db:
        convenio = Convenio(
            id=row['id'],
            nombre=row['nombre'],
            entidad=row['entidad'],
            fecha_vencimiento=datetime.strptime(row['fecha_vencimiento'], '%Y-%m-%d').date(),
            responsable=row['responsable'],
            tipo=row['tipo'],
            renovaciones=row['renovaciones'],
            horas_practica=row['horas_practica'],
            evaluacion_empresa=row['evaluacion_empresa'],
            beneficios=row['beneficios']
        )
        lista_convenios.append(convenio)
    return lista_convenios

def cargar_evaluaciones_desde_db() -> dict[int, list[EvaluacionPractica]]:
    """
    Carga todas las evaluaciones desde la base de datos SQLite.
    """
    conn = get_db_connection()
    evaluaciones_db = conn.execute('SELECT * FROM evaluaciones').fetchall()
    conn.close()

    evaluaciones = {}
    for row in evaluaciones_db:
        evaluacion = EvaluacionPractica(
            id_convenio=row['id_convenio'],
            nombre_estudiante=row['nombre_estudiante'],
            calificacion=row['calificacion'],
            comentarios=row['comentarios']
        )
        if evaluacion.id_convenio not in evaluaciones:
            evaluaciones[evaluacion.id_convenio] = []
        evaluaciones[evaluacion.id_convenio].append(evaluacion)
    return evaluaciones
