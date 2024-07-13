from ScrapingML import ScrapingML

# -----------------------Menú
print("\033c", end="")
print("")
while True:
    print("Menú de búsqueda en MercadoLibre")
    print("    1.-  Buscar por URL 🔗")
    print("    2.-  Buscar por nombre 🔍")
    opcion = input("Opción: ")
    if opcion in ["1", "2"]:
        break
    else:
        print("\033c", end="")
print("")


# ---------------------- Búsqueda según la opción seleccionada	
scraping = None
if opcion == "1":
    url = input("Ingrese la URL de la búsqueda en MercadoLibre: ").replace(" ", "")
    scraping = ScrapingML(url)
elif opcion == "2":
    nombre = input("Ingrese el nombre del producto a buscar en MercadoLibre: ").strip()
    scraping = ScrapingML(nombre, True)
print("")


# ---------------------- Resultados de la búsqueda
if scraping.establecerConexion() and scraping.extraerDatos():
    print(f"🔍: {scraping.getTituloBusqueda()} en Mercadolibre")
    print(f"🔗: {scraping.getUrl()}")
    if scraping.datosEncontrados():
        scraping.graficarPrecios(tipo="todos")
        print("Gráficas ✅")
        scraping.guardarDatosExcel()
        print("Excel ✅")
        scraping.guardarDatosJSON()
        print("JSON ✅")

    else:
        print("❌: No se encontraron datos en la búsqueda de MercadoLibre")
else:
    print("❌: No se pudo establecer conexión con MercadoLibre")
print("")

