import requests
from bs4 import BeautifulSoup

class ScrapingProductoML:
    def __init__(self, url):
        self.url = url
        self.producto = {}
        self.soup = self.ObtenerSoup()
        self.ObtenerProducto()

    def ObtenerSoup(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, 'html.parser')

    def ObtenerProducto(self):
        nombre_tag = self.soup.find('h1', class_='ui-pdp-title')
        precio_tag = self.soup.find('span', class_='andes-money-amount__fraction')
        descripcion_tag = self.soup.find('p', class_='ui-pdp-description__content')
        comentarios_tag = self.soup.find('div', class_='ui-review-capability-comments')
        calificacion_tag = self.soup.find('span', class_='ui-pdp-review__rating')
        comentarios = []
        for comentario in comentarios_tag.find_all('article', class_='ui-review-capability-comments__comment'):
            # la etiqueta p contiene el texto del comentario y tiene la clase ui-review-capability-comments__comment__content ui-review-capability-comments__comment__content
            comentarios.append( comentario.find('p', class_='ui-review-capability-comments__comment__content').text if comentario.find('p', class_='ui-review-capability-comments__comment__content') else "No disponible" )
        
        self.producto['nombre'] = nombre_tag.text if nombre_tag else "No disponible"
        self.producto['precio'] = precio_tag.text if precio_tag else "No disponible"
        self.producto['descripcion'] = descripcion_tag.text if descripcion_tag else "No disponible"
        self.producto['comentarios'] = comentarios
        self.producto['calificacion'] = calificacion_tag.text if calificacion_tag else "No disponible"


    def getProducto(self):
        return self.producto
    def getNombre(self):
        return self.producto['nombre']
    def getPrecio(self):
        return self.producto['precio']
    def getDescripcion(self):
        return self.producto['descripcion']
    def getComentarios(self):
        return self.producto['comentarios']
    def getCalificacion(self):
        return self.producto['calificacion']

if __name__ == "__main__":
    url = "https://www.mercadolibre.com.mx/laptop-gamer-thunderobot-911mt-12th-intel-core-i7-12650h-16gb-de-ram-512gb-ssd-nvidia-geforce-rtx-3050-165-hz-1920x1080px-windows-11-pro/p/MLM28131164#searchVariation%3DMLM28131164%26position%3D4%26search_layout%3Dstack%26type%3Dproduct%26tracking_id%3Dbb395668-a8e7-455b-a09f-f11edff31912"
    producto = ScrapingProductoML(url).getProducto()
    print(producto)
