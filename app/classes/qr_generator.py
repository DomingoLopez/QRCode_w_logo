# Imports de clases
from app.classes.employee import Employee
import numpy as np
import cv2

# Imports de python 
# https://segno.readthedocs.io/en/latest/contact-information.html#vcard
import segno as segno
from segno import helpers
from PIL import Image

'''
Clase QRGenerator. Genera un QR en formato 
vCARD con los datos del empleado
'''
class QRGenerator:
  def __init__(self, empleado: Employee):
    # Empleado
    self.empleado = empleado
    # Imagenes para crear QR
    self.logo = 'app/resources/logo_chroma_rojo.jpg'
    self.output = f'app/resources/output/qr_{empleado.num_emple}.png'
    # Límites máscara QR en BGR
    self.limite_inf_bgr = np.array([0, 0, 150], dtype=np.uint8)
    self.limite_sup_bgr = np.array([100, 100, 255], dtype=np.uint8)
  
  
  '''
  Método para superponer una imagen en otra. 
  En este caso, es un logo que tiene un background concreto, como un chroma
  Y le quitamos el fondo y lo superponemos 
  '''
  def superponer_chroma(self):
    
    error = False
    try:
      
      # Cargamos imágenes
      fondo = cv2.imread(self.output)
      primer_plano = cv2.imread(self.logo)
      primer_plano = cv2.resize(primer_plano, ( ( int(primer_plano.shape[1]*1.5), int(primer_plano.shape[0]*1.5) ) ) )
      # Obtenemos las dimensiones del fondo
      altura, ancho, canales = fondo.shape
      # Obtenemos las dimensiones del primer plano
      altura_1, ancho_1, canales = primer_plano.shape
      
      # La coordenada x e y corresponden con la esquina superior izquierda del logo
      # de la Caja, por lo que para que esté centrado, estas coordenasa las calculamos
      # así
      x, y = (int(altura/2 - altura_1/2),int(ancho/2 - ancho_1/2))

      # Que no sean negativas, que no se salgan de la imagen.
      x = max(x, 0)
      y = max(y, 0)
      # Las coordenadas finales de la esquina superior izquierda
      # de la imagen superpuesta
      
      # Hemos de hacer el mínimo, ya que si no se sale de la imagen
      # El valor de x_fin será o bien menor, o bien igual
      x_fin = min(x + ancho_1, fondo.shape[1])
      y_fin = min(y + altura_1, fondo.shape[0])
      # Calculamos la dimensión del recorte con el que nos quedaremos
      # Si la imagen se sale por eje Y, y_fin será la altura del fondo máximo, etc.
      ancho_recorte = x_fin - x
      altura_recorte = y_fin - y
      # Recortamos lo que se salga, en el fondo
      # Notar que seleccionamos las filas desde y hasta y_fin,
      # y las columnas desde x hasta x_fin de la matriz de la imagen
      recorte_fondo = fondo[y:y_fin, x:x_fin]
      # Recortamos el primer plano, y nos quedamos con lo que es visible
      recorte_primer_plano = primer_plano[:altura_recorte, :ancho_recorte]

      # IMPORTANTE: 
      # Lo suyo sería que el color que pongamos sea el exacto, pero como hay un rango
      # he decidido usar el rango del verde
      # Esto se soluciona pasándole a la función un rango de colores, en vez de solo un color

      lower_red = self.limite_inf_bgr
      upper_red = self.limite_sup_bgr
      mask_chroma = cv2.inRange(recorte_primer_plano, lower_red, upper_red)

      # Aplicamos la máscara sobre el fondo, nos sale praga con el hueco para la chica.
      fondo_con_chroma = cv2.bitwise_and(recorte_fondo, recorte_fondo, mask=mask_chroma)

      # Aplicamos la máscara sobre el primer plano, pero invertida
      primer_plano_con_chroma = cv2.bitwise_and(recorte_primer_plano, recorte_primer_plano, mask=cv2.bitwise_not(mask_chroma))

      # # Superponemos
      resultado = cv2.add(fondo_con_chroma, primer_plano_con_chroma)

      # Añadimos la imagen resultado al fondo
      # No podemos ignorar el recorte del fondo, ya que la máscara tendría distinto tamaño
      # y da error por ello. Por eso se recorta el fondo también, con el mismo ancho y alto
      # que la imagen de la chica recortada.
      fondo[y:y_fin, x:x_fin] = resultado

      cv2.imwrite(self.output, fondo)
      
    except Exception as errorExcept:
      print("Error en creación del QR. Aplicación máscara chroma",errorExcept)
      error = True
    
    return 0 if(not error) else 1
    
    
    
  def generate_qr(self):
    
    name = f'{self.empleado.apellidos};{self.empleado.nombre}'
    displayname=f'{self.empleado.nombre} {self.empleado.apellidos}'
    email = self.empleado.email
    phone = self.empleado.phone

    error = False
    
    try:
      vcard = helpers.make_vcard_data(name=name, 
                                      displayname=displayname,
                                      email=email, 
                                      phone=phone)
      
      qrcode = segno.make(vcard, error='H')
      qrcode.save(self.output, finder_dark='#007857', scale=100)
      
      # Con opencv:
      error = 0 if(self.superponer_chroma() == 0) else 1
      
      
      # # Now open that png image to put the logo
      # img = Image.open(self.output).convert("RGBA")
      # width, height = img.size
      # # How big the logo we want to put in the qr code png
      # logo_size = 1900
      # # Open the logo image
      # logo = Image.open(self.logo).convert("RGBA")
      # # Calculate xmin, ymin, xmax, ymax to put the logo
      # xmin = ymin = int((width / 2) - (logo_size / 2))
      # xmax = ymax = int((width / 2) + (logo_size / 2))
      # # resize the logo as calculated
      # logo = logo.resize((xmax - xmin, ymax - ymin))
      # # put the logo in the qr code
      # img.paste(logo, (xmin, ymin, xmax, ymax))
      # #img.show()
      # img.save(self.output)
    
    except Exception as errorExcept:
      print("Error en la creación del código QR.",errorExcept)
      error = True
    
    return 0 if(not error) else 1
