from pydantic import BaseModel, Field
from typing import List, Optional


class AcceptanceCriteria(BaseModel):
    """
    Modelo para describir los criterios de aceptación de un requisito.
    """
    id: int = Field(..., description="ID único del criterio de aceptación.")
    description: str = Field(..., description="Descripción del criterio de aceptación.")


class SoftwareRequirement(BaseModel):
    """
    Modelo para describir un requisito de software estructurado.
    """
    id: str = Field(..., description="ID único del requisito de software.")
    title: str = Field(..., description="Título del requisito.")
    description: str = Field(..., description="Descripción detallada del requisito.")
    acceptance_criteria: List[AcceptanceCriteria] = Field(
        ..., description="Lista de criterios de aceptación asociados al requisito."
    )
    priority: str = Field(..., description="Prioridad del requisito (Alta, Media, Baja).")
    dependencies: Optional[List[str]] = Field(
        None, description="IDs de otros requisitos de software de los que depende."
    )


class RequirementsPrompt(BaseModel):
    """
    Modelo para estructurar un prompt de IA solicitando requisitos de software.
    """
    context: str = Field(..., description="Contexto o descripción del problema.")
    code_snippet: Optional[str] = Field(
        None, description="Fragmento de código relevante para los requisitos."
    )
    requirements: List[SoftwareRequirement] = Field(
        ..., description="Lista de requisitos de software relacionados."
    )


# # Ejemplo de uso para estructurar un prompt
# example_context = """
# El sistema debe procesar señales de entrada para un interruptor Parkpilot y actualizar su estado en función de una pulsación exclusiva. 
# Se debe asegurar que el interruptor solo cambie a 'Pressed' si ningún otro interruptor está activo.
# """
# example_code_snippet = """
# class ParkpilotSwitch:
#     def __init__(self):
#         self.state = "Released"
#         self.exclusive_press_detected = False

#     def read_input(self, signal_data):
#         parkpilot_signal = signal_data.get("parkpilot_switch", False)
#         other_signals = {key: val for key, val in signal_data.items() if key != "parkpilot_switch"}
#         self.exclusive_press_detected = parkpilot_signal and not any(other_signals.values())

#     def update_state(self):
#         if self.exclusive_press_detected:
#             self.state = "Pressed"
#         else:
#             self.state = "Released"
# """

# example_requirements = [
#     SoftwareRequirement(
#         id="SR-001",
#         title="Actualización del estado del interruptor Parkpilot",
#         description="El sistema debe actualizar el estado del objeto `ParkpilotSwitch` en función de la señal de entrada recibida. Si el interruptor de Parkpilot está presionado y ningún otro interruptor está activo, el estado debe cambiar a 'Pressed'. Si no se cumplen estas condiciones, el estado debe permanecer o cambiar a 'Released'.",
#         acceptance_criteria=[
#             AcceptanceCriteria(id=1, description="El estado cambia a 'Pressed' si solo está activo 'parkpilot_switch'."),
#             AcceptanceCriteria(id=2, description="El estado cambia a 'Released' si cualquier otro interruptor está activo."),
#         ],
#         priority="Alta",
#         dependencies=None,
#     ),
#     SoftwareRequirement(
#         id="SR-002",
#         title="Detección de pulsación exclusiva del interruptor Parkpilot",
#         description="El sistema debe implementar una lógica que evalúe si el interruptor de Parkpilot está presionado exclusivamente, sin que ningún otro interruptor o señal esté activa.",
#         acceptance_criteria=[
#             AcceptanceCriteria(id=1, description="La pulsación exclusiva detecta 'True' solo si ningún otro interruptor está activo."),
#             AcceptanceCriteria(id=2, description="Si algún otro interruptor está activo, la pulsación exclusiva detecta 'False'."),
#         ],
#         priority="Media",
#         dependencies=["SR-001"],
#     )
# ]

# prompt = RequirementsPrompt(
#     context=example_context,
#     code_snippet=example_code_snippet,
#     requirements=example_requirements,
# )

# # Convertir a JSON para enviar a una IA
# print(prompt.json(indent=4))
