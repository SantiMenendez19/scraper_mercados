import json

# Lectura del json de configuracion
def read_json_conf(json_file):
    with open(json_file) as json_data:
        json_conf = json.load(json_data)
        return json_conf

# Reemplazar acentos
def replace_acentos(text):
    text = text.replace("á", "a")
    text = text.replace("é", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o")
    text = text.replace("ú", "u")
    text = text.replace("ñ", "n")
    text = text.replace(" ", "-")
    return text