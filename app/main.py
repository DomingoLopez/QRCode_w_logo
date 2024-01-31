from typing import Union
from fastapi import FastAPI

# FastApi example, skeleton
# https://medium.com/@ketansomvanshi007/structuring-a-fastapi-app-an-in-depth-guide-cdec3b8f4710

# Lanzar el server: uvicorn app.main:app --reload (para recargar ante cambios)
# Ver la ruta donde se genera la documentación. http://127.0.0.1:8000/docs (Hecho con swagger)
# Ver documentación alternativa: http://127.0.0.1:8000/redoc (Hecho con Redoc)
from app.app import create_app

app = create_app()
