# main.py

import csv
from datetime import datetime
# Importamos las clases y funciones que creamos en el otro archivo
from modelos import Convenio, analizar_convenio, EstadoConvenio

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
                # Convierte la fecha de texto (YYYY-MM-DD) a objeto date
                fecha_vencimiento=datetime.strptime(fila['fecha_vencimiento'], '%Y-%m-%d').date(),
                responsable=fila['responsable'],
                # Convierte horas a entero si existe, si no, es None
                horas_practica=int(fila['horas_practica']) if fila['horas_practica'] else None,
                evaluacion_empresa=fila['evaluacion_empresa'] or None,
                beneficios=fila['beneficios'] or None
            )
            lista_convenios.append(convenio)
    return lista_convenios

def procesar_y_mostrar_convenios():
    """
    Función principal que carga los convenios desde el CSV y muestra su estado.
    """
    print("--- Iniciando sistema de gestión de Convenios ---")
    
    try:
        # 1. Cargar los datos desde el archivo
        convenios = cargar_convenios_desde_csv('convenios.csv')
        print(f"Se cargaron {len(convenios)} convenios desde el archivo.")
        
        # --- Reporte General ---
        print("\n--- Reporte de Estado de Convenios (Semáforo) ---")
        convenios_urgentes = []
        for convenio in convenios:
            analisis = analizar_convenio(convenio.fecha_vencimiento)
            
            # Formateo del mensaje de días
            if analisis.dias_restantes >= 0:
                mensaje_dias = f"(Vence en {analisis.dias_restantes} días)"
            else:
                mensaje_dias = f"(Vencido hace {-analisis.dias_restantes} días)"

            print(f"Convenio: '{convenio.nombre}' -> Estado: {analisis.estado.value} {mensaje_dias}")

            # Si el convenio es Amarillo o Rojo, lo guardamos para el reporte de urgencia
            if analisis.estado in [EstadoConvenio.AMARILLO, EstadoConvenio.ROJO]:
                convenios_urgentes.append((convenio, analisis))

        # --- Reporte de Acciones Urgentes ---
        print("\n--- Reporte de Acciones Urgentes (Prioridad Alta) ---")
        if not convenios_urgentes:
            print("¡Excelente! No hay convenios que requieran atención inmediata.")
        else:
            # Ordenamos por los que vencen antes
            convenios_urgentes.sort(key=lambda item: item[1].dias_restantes)
            for convenio, analisis in convenios_urgentes:
                print(f"[!] '{convenio.nombre}' -> {analisis.estado.value}. Vence en {analisis.dias_restantes} días.")

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'convenios.csv'. Asegúrate de que exista en la misma carpeta.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    print("\n--- Simulación finalizada ---")


# Este bloque asegura que el código solo se ejecute cuando corres este archivo directamente
if __name__ == "__main__":
    procesar_y_mostrar_convenios()
