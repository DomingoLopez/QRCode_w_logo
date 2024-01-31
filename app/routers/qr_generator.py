# Imports de fastApi
import sys
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
# Imports del proyecto
from app.classes.employee import Employee
from app.classes.qr_generator import QRGenerator


router = APIRouter(prefix="/qr_generator", tags=["qr_generator"])

@router.get("/")
async def generate_qr(num_emple: str, 
                      nombre: str,
                      apellidos: str, 
                      email: str, 
                      phone: str, 
                      centro:str,
                      nomcentro:str,
                      puesto_plantilla: str):
    
    emp = Employee(num_emple,nombre,apellidos,email,phone, 
                    centro,nomcentro,puesto_plantilla)
    
    qr_generator = QRGenerator(emp)
    
    error_code = qr_generator.generate_qr()
    
    if(error_code == 0):
        # Si todo ok al generar, devuelvo la imagen
        image_path = f"app\\resources\output\qr_{emp.num_emple}.png"
        image_path_sys = os.path.join(sys.path[0], image_path)
        return FileResponse(image_path_sys)
    else:
        # Si no, devuelvo error
        return {"error":"El QR no pudo ser creado o encontrado "}



