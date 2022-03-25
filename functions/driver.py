## Para Chrome
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.options import Options as Chrome_options
## Para Edge (chromium)
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver

import json
import os
import sys

## Opciones del driver e inicializacion
# Chrome
def start_chrome_driver():
    CHROME_DRIVER_PATH = os.path.join(os.path.dirname(sys.argv[0]), "driver", "chromedriver.exe")
    options = Options()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    return driver

# Edge
def start_edge_driver():
    EDGE_DRIVER_PATH = os.path.join(os.path.dirname(sys.argv[0]), "driver", "msedgedriver.exe")
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = Edge(executable_path=EDGE_DRIVER_PATH, options=options)
    return driver