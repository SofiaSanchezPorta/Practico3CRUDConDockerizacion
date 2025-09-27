import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina


def run(*args):
    if not args:
        print("Error. Favor de proporcionar la ruta del archivo CSV.")
        print("Uso: ./manage.py runscript importar_oficinas --scripts-arg <ruta_del_archivo_csv>")
        sys.exit(1)

    csv_file = args[0]

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            oficinas_a_crear = []

            for row in reader:
                nombre = row.get('nombre').strip()
                nombre_corto = row.get('nombre_corto').strip()

                if not nombre or not nombre_corto:
                    print(f"Error en la fila {row}. Falta un campo.")
                    continue

                try:
                    oficina = Oficina(nombre=nombre, nombre_corto=nombre_corto)
                    oficina.full_clean()  # Validar los datos
                    oficinas_a_crear.append(oficina)
                except ValidationError as e:
                    print(f"Error de validaciónen la fila {row}. Detalle: {e}")
                except Exception as e:
                    print(f"Error inesperado en fila {row}. Detalle: {e}")
            with transaction.atomic():
                Oficina.objects.bulk_create(oficinas_a_crear)
                print(f"{len(oficinas_a_crear)} oficinas importadas exitosamente.")
    
    except FileNotFoundError:
        print(f"No se encontró el archivo {csv_file}")
    except csv.Error as e:
        print(f"Ocurrió un error inesperado en la importación del archivo CSV: {e}")
