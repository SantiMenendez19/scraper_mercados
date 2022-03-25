from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
import sys

# Tomar las categorias de la pagina de dia
def get_categories_dia(driver, link):
    driver.get(link)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    categorias = soup.find("ul", {"class": "dropdown-menu"})
    categorias = categorias.find_all("li")
    list_categorias = []
    for categoria in categorias:
        categoria = categoria.find("a")
        tipo = categoria.span
        if tipo is not None:
            link = categoria.get("href")
            list_categorias.append((tipo.text, link))
    return list_categorias

# Busqueda por categoria
def find_products_categories_dia(driver, category, link, logger):
    # Fecha actual
    date_now = datetime.now().strftime("%Y-%m-%d")
    hour_now = datetime.now().strftime("%H:%M:%S")
    retries = 3
    retry = True
    while retry:
        try:
            print(f"Categoria: {category}")
            # Ingreso a la pagina
            driver.get(f"{link}/{category}")
            time.sleep(5)

            # Quitar el pop-up de envio (si existe)
            #try:
            #    driver.execute_script("document.getElementsByClassName('shipping__schedule__step--close')[0].click()")
            #except BaseException:
            #    print(f"No se encontro el elemento de seleccionar tipo de envio en la categoria {categoria}")

            # Abrir el boton de mas productos
            #try:
            #    while True:
            #        driver.find_element_by_class_name("viewMoreProds").click()
            #        time.sleep(2)
            #except BaseException:
            #    logger_info.info(f"No se encontraron mas productos para {categoria}")
            #    print(f"No se encontraron mas productos para {categoria}")

            # Scrollear hasta que carguen todos los productos
            last_height = driver.execute_script("return document.body.scrollHeight")
            try:
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    scroll_height = driver.execute_script("return document.body.scrollHeight")
                    if scroll_height == last_height:
                        raise Exception("No hay mas productos")
                    else:
                        last_height = scroll_height

            except BaseException:
                logger.info(f"No se encontraron mas productos para {category}")
                print(f"No se encontraron mas productos para {category}")       

            # Leer con bs4 el html y obtener producto, marca, link y precio
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html5lib")
            products = soup.find("div", {"class" : "vitrine resultItemsWrapper"})
            products = products.find_all("ul")
            list_products = []
            for product in products:
                # nombre, link y precio
                soup_nombre = product.find("div", {"class" : "product-name"})
                if soup_nombre is not None:
                    nombre = soup_nombre.find("a").get("title")
                    link = soup_nombre.find("a").get("href")
                else:
                    continue
                # marca
                soup_marca = product.find("div", {"class" : "marca"})
                if soup_marca is not None:
                    marca = soup_marca.text
                    marca = marca.replace("\n","")
                    marca = marca.strip()
                else:
                    marca = None
                # precio
                soup_precio = product.find("div", {"class" : "price"})
                if soup_precio is not None:
                    precio = soup_precio.find("span").text
                else:
                    precio = None
                # cantidades
                soup_quantity = product.find("div", {"class" : "new_quantity"})
                if soup_quantity is not None:
                    stock = soup_quantity.find("span").get("data-maxqty")
                else:
                    stock = None
                list_products.append((nombre, marca, link, precio, stock))

            # Guardado en archivo
            hour_file = hour_now.replace(":","")
            with open(os.path.join(os.path.dirname(sys.argv[0]), "output", f"productos_dia_{category}_{date_now}_{hour_file}.csv"), "wt", encoding="utf-8-sig") as f:
                print(f"Cantidad de productos: {len(list_products)}")
                logger.info(f"Cantidad de productos: {len(list_products)}")
                f.write("nombre|stock|precio|marca|link|hora|fecha" + "\n")
                for product in list_products:
                    f.write(product[0] + 
                            "|" + 
                            product[4] +
                            "|" +
                            product[3].replace("$","").replace(",",".").strip() + 
                            "|" +
                            product[1] +
                            "|" +
                            product[2] +
                            "|" +
                            hour_now +
                            "|" +
                            date_now +
                            "\n")
            logger.info(f"Productos guardados correctamente con el nombre productos_dia_{category}_{date_now}_{hour_file}.csv")
            with open(os.path.join(os.path.dirname(sys.argv[0]), "output", f"proceso_dia_{date_now}.csv"), "a", encoding="utf-8-sig") as f:
                f.write(category + "|" + "TERMINADO" + "|" + hour_now + "|" + "" + "\n")
            retry = False
            driver.quit()
        except BaseException as err:
            logger.error(f"Error en la categoria {category}")
            logger.error(f"Error arrojado: {err}")
            logger.error(f"Reintentos restantes: {retries}")
            logger.error(f"Se volvera a reintentar el scraping de la categoria {category}")
            retries -= 1
            if retries == 0:
                retry = False
            if not retry:
                with open(os.path.join(os.path.dirname(sys.argv[0]), "output", f"proceso_dia_{date_now}.csv"), "a", encoding="utf-8-sig") as f:
                    f.write(category + "|" + "ERROR" + "|" + hour_now + "|" + err + "\n")
                driver.quit()