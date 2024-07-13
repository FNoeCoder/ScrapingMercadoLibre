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
                nombre_tag = product.find("h2", class_="ui-search-item__title")
                nombre = nombre_tag.text.strip() if nombre_tag else "No disponible"
                
                precio_tag = product.find("span", class_="andes-money-amount__fraction")
                precio = precio_tag.text.strip() if precio_tag else "No disponible"
                
                enlace_tag = product.find("a", class_="ui-search-item__group__element ui-search-link__title-card ui-search-link")
                enlace = enlace_tag["href"] if enlace_tag else "No disponible"
                
                imagen_tag = product.find("img", class_="ui-search-result-image__element")
                imagenEnlace = imagen_tag["data-src"] if imagen_tag else "No disponible"
                
                descripcion = ScrapingProductoML(enlace).getProducto()["descripcion"] if enlace != "No disponible" else "No disponible"

                if precio != "No disponible":
                    self.precios.append(float(precio.replace(",", "")))
                print(precio)
                self.data.append({  # Agregar los detalles del producto como un diccionario a la lista de datos
                    "Nombre": nombre,
                    "Precio": precio,
                    "Enlace": enlace,
                    "Imagen": imagenEnlace, 
                    "Descripcion": descripcion
                })
            self.calcularPrecioPromedio()
            return True
        else:
            return False
    def calcularPrecioPromedio(self):
        if len(self.precios) > 0:
            self.precioPromedio = sum(self.precios) / len(self.precios)
            #redondear a 2 decimales
            self.precioPromedio = round(self.precioPromedio, 2)
            return True
        else:
            return False

    def guardarDatosExcel(self):
        if self.conexionEstablecida:
            df = pd.DataFrame(self.data)  # Crear DataFrame a partir de la lista de diccionarios
            # Crear un DataFrame con el precio promedio
            df_precio_promedio = pd.DataFrame([{
                "Nombre": "Precio promedio",
                "Precio": self.precioPromedio,
                "Enlace": "",
                "Imagen": "",
                "Descripcion": ""
            }])
            # Concatenar el DataFrame original con el del precio promedio
            df = pd.concat([df, df_precio_promedio], ignore_index=True)
            df.to_excel(f"./Archivos_Generados/Excel/{self.tituloBusqueda.replace(" ", "_")}.xlsx", index=False)
            return True
        else:
            return False
    def guardarDatosJSON(self):
        if self.conexionEstablecida:
            with open(f"./Archivos_Generados/JSON/{self.tituloBusqueda.replace(" ", "_")}.json", "w", encoding="utf-8") as file:
                json.dump({
                    "Titulo de la busqueda": self.tituloBusqueda,
                    "Datos": self.data,
                    "Precio promedio": self.precioPromedio
                }, file, ensure_ascii=False, indent=4)
            return True
        else:
            return False
    def graficarPrecios(self, tipo = "cercanos"):
        if len(self.precios) > 0:
            self.productosSeleccionados = self.data
            if "baratos" == tipo:
                self.productosSeleccionados = self.getDatosMasBarato()
            elif "caros" == tipo:
                self.productosSeleccionados = self.getDatosMasCaro()
            elif "cercanos" == tipo:
                self.productosSeleccionados = self.getDatosMasCercaPromedio()
            elif "todos" == tipo:
                self.productosSeleccionados = self.data
            else:
                return False

            plt.figure(figsize=(20, 10))
            plt.bar([producto["Nombre"][:15] for producto in self.productosSeleccionados], [float(producto["Precio"].replace(",", "")) for producto in self.productosSeleccionados], color="skyblue", label="Precio")
            plt.axhline(y=self.precioPromedio, color='r', linestyle='-', label=f"Precio promedio: ${self.precioPromedio}")
            plt.xticks(rotation=90)
            plt.xlabel("Productos")
            plt.ylabel("Precio")
            plt.title(f"Precios de {self.tituloBusqueda} (más {tipo})")
            plt.xticks(fontsize=20)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"./Archivos_Generados/IMG/{self.tituloBusqueda.replace(' ', '_')}_{tipo}.png")
            plt.close()
            del self.productosSeleccionados
            return True
        else:
            return False
    def datosEncontrados(self):
        return len(self.data) > 0
    def getDatosMasBarato(self):
        if len(self.data) > 0:
            # Obtener los 10 productos más baratos
            return sorted(self.data, key=lambda x: float(x["Precio"].replace(",", "")))[:10]
        else:
            return None
    def getDatosMasCaro(self):
        if len(self.data) > 0:
            # Obtener los 10 productos más caros
            return sorted(self.data, key=lambda x: float(x["Precio"].replace(",", "")), reverse=True)[:10]
        else:
            return None
    def getDatosMasCercaPromedio(self):
        if len(self.data) > 0:
            # Obtener los 10 productos más cercanos al precio promedio
            return sorted(self.data, key=lambda x: abs(float(x["Precio"].replace(",", "")) - self.precioPromedio))[:10]
        else:
            return None

# # url directamente de la página
# url = "https://listado.mercadolibre.com.mx/laptop-gamer#D[A:laptop%20gamer]"
# scraping = ScrapingML(url)


# if scraping.establecerConexion() and scraping.extraerDatos():
#     print("Datos extraídos correctamente")
#     scraping.guardarDatosExcel()
#     scraping.guardarDatosJSON()
#     scraping.graficarPrecios(tipo="todos")
#     print("Datos guardados correctamente")
# else:
#     print("Error al establecer la conexión o extraer datos")

