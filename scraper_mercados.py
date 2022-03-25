# Imports
# Natives
import os, sys
# fechas
from datetime import datetime
# threads
import threading
# logs
import logging

# Functions
from functions.driver import start_chrome_driver, start_edge_driver
from functions.scraper_dia import find_products_categories_dia
from functions.misc import read_json_conf, replace_acentos

# DIA
def start_scraper_dia():
    date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger_file_debug = f"log_scraping_dia-DEBUG-{date_now}.log"
    logger_file_info = f"log_scraping_dia-INFO-{date_now}.log"
    config_json_file = "conf_scraper_dia.json"
    scrapper_page = "DIA"

    # Create folders if not exists
    if not os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), "log")):
        os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"))
    if not os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), "output")):
        os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "output"))

    # Logging
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", logger_file_debug), filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("INFO")
    logger.setLevel(logging.INFO)
    filehandler = logging.FileHandler(os.path.join(os.path.dirname(sys.argv[0]), "log", logger_file_info), "w")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    
    logger.info(f"Inicio del scraping de {scrapper_page}")

    # Lectura de archivo de configuracion
    json_conf = os.path.join(os.path.dirname(sys.argv[0]), "conf", config_json_file)
    json_conf = read_json_conf(json_conf)
    logger.info("Archivo de configuracion leido correctamente")

    # Toma de categorias de la configuracion
    categories = json_conf["categorias"]
    link = json_conf["link"]

    # Busqueda por categorias
    threads = []
    for cat in categories:
        # Inicializacion del driver
        logger.info(f"Inicializacion del driver para la categoria {cat}")
        driver = start_edge_driver()
        thread = threading.Thread(target=find_products_categories_dia, args=(driver, cat, link, logger))
        thread.start()
        threads.append(thread)
    
    # Espera a que terminen los threads
    for thread in threads:
        thread.join()

    # Informo en el log los threads terminados
    logger.info("Se terminaron de buscar todas las categorias")
    logger.info(f"Fin del scraping de {scrapper_page}")

# Main
if __name__ == "__main__":
    start_scraper_dia()
    sys.exit(0)

