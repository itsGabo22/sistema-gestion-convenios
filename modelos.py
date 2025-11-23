# modelos.py

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
    horas_practica: Optional[int] = None    
    evaluacion_empresa: Optional[str] = None
    beneficios: Optional[str] = None

# Nueva estructura para el resultado del análisis
@dataclass
class AnalisisConvenio:
    """
    Contiene el resultado del análisis de estado de un convenio.
    """
    estado: 'EstadoConvenio'
    dias_restantes: int

# 2. Enumeración para los estados del semáforo
class EstadoConvenio(Enum):
    """
    Define los posibles estados de un convenio según su fecha de vencimiento.
    """
    VERDE = "Verde"
    AMARILLO = "Amarillo"
    ROJO = "Rojo"

# 3. Lógica de negocio para determinar el estado
def analizar_convenio(fecha_vencimiento: date) -> AnalisisConvenio:
    """
    Calcula el estado de un convenio y los días restantes para su vencimiento.

    Retorna un objeto AnalisisConvenio con el estado y los días.
    """
    hoy = date.today()
    diferencia_dias = (fecha_vencimiento - hoy).days

    # Aproximación de meses considerando 30.44 días por mes en promedio
    meses_restantes = diferencia_dias / 30.44
    estado_actual: EstadoConvenio

    if diferencia_dias > 120: # Más de 4 meses
        estado_actual = EstadoConvenio.VERDE
    elif 60 <= diferencia_dias <= 120: # Entre 2 y 4 meses
        estado_actual = EstadoConvenio.AMARILLO
    else:
        estado_actual = EstadoConvenio.ROJO # Menos de 2 meses o vencido
    
    return AnalisisConvenio(estado=estado_actual, dias_restantes=diferencia_dias)

def cargar_convenios_desde_csv(ruta_archivo: str) -> list[Convenio]:
    """
    Lee un archivo CSV y carga los datos en una lista de objetos Convenio.
    """
    lista_convenios = []
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            # Convierte los datos del CSV al tipo correcto
            convenio = Convenio(
                id=int(fila['id']),
                nombre=fila['nombre'],
                entidad=fila['entidad'],
                fecha_vencimiento=datetime.strptime(fila['fecha_vencimiento'], '%Y-%m-%d').date(),
                responsable=fila['responsable'],
                horas_practica=int(fila['horas_practica']) if fila['horas_practica'] else None,
                evaluacion_empresa=fila['evaluacion_empresa'] or None,
                beneficios=fila['beneficios'] or None
            )
            lista_convenios.append(convenio)
    return lista_convenios
