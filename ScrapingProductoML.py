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
        if comentarios_tag is not None:
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
    links = [
        "https://www.mercadolibre.com.mx/laptop-hp-245-g9-amd-ryzen-3-3250u-hasta-35-ghz-memoria-ram-de-16-gb-ddr4-ssd-256-gb-windows-11-home-64-bit-teclado-en-espanol-14-pulgadas-negro/p/MLM28615515#searchVariation%3DMLM28615515%26position%3D6%26search_layout%3Dstack%26type%3Dproduct%26tracking_id%3D3b5f94a5-51e6-4114-b50a-a7155fc3fe66",
        "https://www.mercadolibre.com.mx/laptop-dell-inspiron-3535-ryzen-5-7520u-512gb-ssd-8gb-ddr5-color-plateado/p/MLM30164862?pdp_filters=item_id:MLM2960561446#polycard_client=recommendations_pdp-pads-up&reco_backend=recos-merge-experimental-pdp-up-a_marketplace&reco_client=pdp-pads-up&reco_item_pos=0&reco_backend_type=low_level&reco_id=900044b1-d871-4e40-8231-cdf3a880d4f8&wid=MLM2960561446&sid=recos&is_advertising=true&ad_domain=PDPDESKTOP_UP&ad_position=1&ad_click_id=YmNjOGQ0ZmMtZWMzMi00OThmLTgyNzAtNDJiZjVkYWQ0Njkx",
        "https://articulo.mercadolibre.com.mx/MLM-2055628443-laptop-hp-240-g9-intel-core-i3-1215u-16gb-1tb-ssd-m2-14-w11-_JM#polycard_client=recommendations_pdp-pads-up&reco_backend=recos-merge-experimental-pdp-up-a_marketplace&reco_client=pdp-pads-up&reco_item_pos=1&reco_backend_type=low_level&reco_id=af40e7af-148e-4733-9051-e8845efda041&is_advertising=true&ad_domain=PDPDESKTOP_UP&ad_position=2&ad_click_id=M2NkMjliOTgtOTczNy00ZDcwLWJmMWUtNzExYzAxM2IyMGI3",
        "https://www.mercadolibre.com.mx/laptop-gamer-thunderobot-911mt-12th-intel-core-i7-12650h-16gb-de-ram-512gb-ssd-nvidia-geforce-rtx-3050-165-hz-1920x1080px-windows-11-pro/p/MLM28131164#searchVariation%3DMLM28131164%26position%3D4%26search_layout%3Dstack%26type%3Dproduct%26tracking_id%3Dbb395668-a8e7-455b-a09f-f11edff31912"
    ]
    #imprimir el precio de cada producto
    for link in links:
        producto = ScrapingProductoML(link)
        # print(producto.getNombre())
        print(producto.getPrecio())
        # print(producto.getDescripcion())
        # print(producto.getComentarios())
        # print(producto.getCalificacion())
        print("")
