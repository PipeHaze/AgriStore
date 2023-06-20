from PIL import Image
from django.conf import settings

def resize_image(image):
    # Obtener el tamaño predeterminado de las imágenes
    default_width = settings.DEFAULT_WIDTH
    default_height = settings.DEFAULT_HEIGHT

    # Abrir la imagen utilizando Pillow
    img = Image.open(image)

    # Redimensionar la imagen al tamaño predeterminado
    img.thumbnail((default_width, default_height), Image.ANTIALIAS)

    # Guardar la imagen redimensionada
    img.save(image.path)