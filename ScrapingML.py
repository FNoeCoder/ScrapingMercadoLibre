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
        self.precios = []
        self.precioPromedio = 0
        self.mediana = 0
        self.desviacionEstandar = 0

    def getTituloBusqueda(self):
        return self.tituloBusqueda
    def getUrl(self):
        return self.url
    def establecerConexion(self):
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.conexionEstablecida = self.response.status_code == 200
        return self.conexionEstablecida
    
    def extraerDatos(self):
        if self.conexionEstablecida:
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
            

                if precio != "No disponible":
                    self.precios.append(float(precio.replace(",", "")))
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
            return True
        else:
            return False

    def guardarDatosJSON(self):
        if self.conexionEstablecida:
            with open(f"./Archivos_Generados/JSON/{self.tituloBusqueda.replace(" ", "_")}.json", "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            return True
        else:
            return False

    def datosEncontrados(self):
        return len(self.data) > 0



