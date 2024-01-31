import os
import sys
import pytest
import logging

# Obtener la ruta del directorio actual del script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Agregar el directorio padre al sys.path
parent_directory = os.path.abspath(os.path.join(current_directory, '../..'))
sys.path.append(parent_directory)

# Importación de rutas necesarias tras añadir al path
# Importamos lo necesario para testear clase qr_generator
from app.classes.employee import Employee
from app.classes.qr_generator import QRGenerator


# Get logger
logger = logging.getLogger('__qr_generator__')
logger.setLevel(logging.INFO)

emp = Employee(
    num_emple=1574,
    nombre='Domingo',
    apellidos='López Pacheco',
    email='domingolp@crgranada.com',
    phone='637447471',
    centro=9352,
    nomcentro='CI Desarrollo',
    puesto_plantilla='Técnico'
)


def test_creation():
    
    qr = QRGenerator(emp)
    assert qr.empleado == emp, "Debería ser igual. Objeto creado de forma correcta"

def test_qr_generation():
    
    qr = QRGenerator(emp)
    result = qr.generate_qr()
    
    assert result == 0, "Resultado debería ser 0. Ejecución correcta"

    
