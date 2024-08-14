from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
from urllib.parse import quote
from ScrapingProductoML import ScrapingProductoML
import matplotlib.pyplot as plt

class ScrapingML:
    def __init__(self, url, busquedaPersonalizada = False):
        if (busquedaPersonalizada is False):
            self.url = url
        else:
            self.texto = url.lower()
            self.texto = quote(self.texto, safe='')
            self.texto = self.texto.replace('%20', ' ')
            self.url = f"https://listado.mercadolibre.com.mx/{self.texto.replace(' ', '-')}#D[A:{self.texto.replace(' ', '%20')}]"
            del self.texto

        self.data = []
        self.response = None
        self.soup = None
        self.conexionEstablecida = False
        self.tituloBusqueda = ""
        self.URLsPaginacion = []
        self.establecerConexion(self.url)
        if self.conexionEstablecida:
            self.URLsPaginacion = self.getURLsPaginacion()
            for url in self.URLsPaginacion:
                self.establecerConexion(url)
                self.extraerDatos()

    def getURLsPaginacion(self):
        return self.URLsPaginacion
    def getTituloBusqueda(self):
        return self.tituloBusqueda
    def getUrl(self):
        return self.url
    def establecerConexion(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.conexionEstablecida = self.response.status_code == 200
        return self.conexionEstablecida
    
    def extraerDatos(self):
        products = self.soup.find_all("div", class_="andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16")
        if len(products) == 0:
            products = self.soup.find_all("div", class_="andes-card ui-search-result ui-search-result--core andes-card--flat andes-card--padding-16 andes-card--animated")

        titulo_input = self.soup.find("input", class_="nav-search-input")
        self.tituloBusqueda = titulo_input["value"] if titulo_input else "No disponible"

        for product in products:
            enlace_tag = product.find("a", class_="ui-search-item__group__element ui-search-link__title-card ui-search-link")
            enlace = enlace_tag["href"] if enlace_tag else "No disponible"

            producto = ScrapingProductoML(enlace)
            nombre = producto.getNombre()
            precio = producto.getPrecio()
            descripcion = producto.getDescripcion()
            comentarios = producto.getComentarios()
            calificacion = producto.getCalificacion()
            imagen_tag = product.find("img", class_="ui-search-result-image__element")
            imagenEnlace = imagen_tag["data-src"] if imagen_tag else "No disponible"
        

            print(precio)
            self.data.append({  # Agregar los detalles del producto como un diccionario a la lista de datos
                "Nombre": nombre,
                "Precio": precio,
                "Enlace": enlace,
                "ImagenPortada": imagenEnlace, 
                "Descripcion": descripcion,
                "Comentarios": comentarios,
                "Calificacion": calificacion,
            })



    def guardarDatosJSON(self):
        if self.conexionEstablecida:
            with open(f"./{self.tituloBusqueda.replace(" ", "_")}.json", "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            return True
        else:
            return False
    def getURLsPaginacion(self):
        links = []
        if self.conexionEstablecida:
            paginacion = self.soup.find("ul", class_="andes-pagination ui-search-andes-pagination andes-pagination--large") 
            if paginacion:
                for link in paginacion.find_all("a", class_="andes-pagination__link"):
                    links.append(link["href"])
            else:
                links.append(self.url)
            links.pop(0)
        return links


    def datosEncontrados(self):
        return len(self.data) > 0


if __name__ == "__main__":
    url = "https://listado.mercadolibre.com.mx/laptpo#D[A:laptpo]"
    scraping = ScrapingML(url)
    print(scraping.getTituloBusqueda())
    scraping.guardarDatosJSON()



