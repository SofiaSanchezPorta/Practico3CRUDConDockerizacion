import csv
import sys
from django.db import transaction
from django.forms import ValidationError
from oficina.models import Oficina
from persona.models import Persona


def run(*args):
    if not args:
        print("Error. Favor de proporcionar la ruta del archivo CSV.")
        print("Uso: ./manage.py runscript import_personas --scripts-arg <ruta_del_archivo_csv>")
        sys.exit(1)

    csv_file = args[0]

    oficinas_map = {oficina.nombre_corto: oficina for oficina in Oficina.objects.all()}

    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            personas_a_crear = []

            for row in reader:
                nombre = row.get('nombre').strip()
                apellido = row.get('apellido').strip()
                edad = row.get('edad').strip()
                oficina_nombre_corto = row.get('oficina_nombre_corto').strip()

                if not nombre or not apellido or not edad or not oficina_nombre_corto:
                    print(f"Error en la fila {row}. Falta un campo.")
                    continue

                try:
                    edad_int = int(edad)
                except (ValueError, TypeError):
                    print(f"Error en la fila {row}. La edad no es un número válido.")
                    continue

                oficina_obj = None
                if oficina_nombre_corto:
                    oficina_obj = oficinas_map.get(oficina_nombre_corto)
                    if not oficina_obj:
                        print(f"Advertencia. No existe la oficina mencionada {oficina_nombre_corto} en Fila: {row}")
                        print(f"Se creará el registro sin oficina.")

                try:
                    persona = Persona(nombre=nombre, apellido=apellido, edad=int(edad), oficina=oficina_obj)
                    persona.full_clean()
                    personas_a_crear.append(persona)
                except ValidationError as e:
                    print(f"Error de validaciónen la fila {row}. Detalle: {e}")
                except Exception as e:
                    print(f"Error inesperado en fila {row}. Detalle: {e}")
            with transaction.atomic():
                Persona.objects.bulk_create(personas_a_crear)
                print(f"Se importaron {len(personas_a_crear)} personas exitosamente.")

    except FileNotFoundError:
        print(f"No se encontró el archivo {csv_file}")
    except csv.Error as e:
        print(f"Ocurrió un error inesperado en la importación del archivo CSV: {e}")
