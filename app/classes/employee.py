'''
Clase empleado, que define un empleado con su num_emple,
nombre, apellidos, teléfono, centro, y puesto
'''
class Employee:
  def __init__(self, num_emple: str, 
                      nombre: str, 
                      apellidos: str, 
                      email: str, 
                      phone: str, 
                      centro:str,
                      nomcentro:str,
                      puesto_plantilla: str):
    self.num_emple = num_emple
    self.nombre = nombre
    self.apellidos = apellidos
    self.email = email
    self.phone = phone
    self.centro = centro
    self.nomcentro = nomcentro
    self.puesto_plantilla = puesto_plantilla
