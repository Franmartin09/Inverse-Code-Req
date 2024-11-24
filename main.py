from config import config_groq, config_variables
from extract_code import generate_chunks
from request_req import generate_requirements
from datetime import datetime
import os 
import json

#Run Config
groq = config_groq()
dir_code, output_dir = config_variables()

#Extract Functions Code
code_context = generate_chunks(dir_code)

array_final=[]
for i, chunk in enumerate(code_context):

    respuesta = generate_requirements(chunk, groq)
    array_final.append(respuesta)

# Generar un nombre de archivo basado en la fecha y hora actual
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_dir, f"{timestamp}.json")

# Guardar array_final en un archivo JSON
array_final = []

for i, chunk in enumerate(code_context):
    respuesta = generate_requirements(chunk, groq)
    array_final.append(respuesta)

# Guardar en JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(array_final, f, ensure_ascii=False, indent=4)