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


