from pydantic import ValidationError
from model import SoftwareRequirement
import json

def generate_requirements(code: str, groq_client):
    # Construcción del mensaje del sistema y del usuario
    system_message = f"""
        You are a Requirement Engineer assistant with knowledge of code and the IREB structure for software requirement.
        Here is the code as context:
        {code}
        You must understand the code and generate software requirement in JSON format following this structure:
        {json.dumps(SoftwareRequirement.model_json_schema(), indent=8)}
    """

    user_message = "Write software requirement based on the provided code."

    # Llamada a Groq para generar las respuestas
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        model="llama-3.1-70b-versatile",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"},  # Solicitamos el formato JSON directamente
    )

    # Obtener el contenido de la respuesta
    response = chat_completion.choices[0].message.content

    if response:
        try:
            # Validar la respuesta generada contra el modelo Pydantic
            requirement = SoftwareRequirement.model_validate_json(response)
            return requirement.model_dump()
        except ValidationError as e:
            print("Validation Error:", e.json(indent=4))
            return "The response did not match the expected structure."
    else:
        return "No relevant results were found."
