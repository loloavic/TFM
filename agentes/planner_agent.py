# agentes/planner_agent.py

from typing import List, Optional
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field

class Step(BaseModel):
    titulo: str
    documentos: List[str] = Field(default_factory=list)
    responsable: Optional[str] = None
    formulario: Optional[str] = None

class Plan(BaseModel):
    title: str
    steps: List[Step]
    recomendaciones: List[str] = Field(default_factory=list)

SYSTEM_PROMPT = (
    "Eres un planificador de trámites administrativos orientado a eventos vitales, "
    "centrado en el usuario (user-first). Devuelve SIEMPRE JSON válido que cumpla el esquema Plan. "
    "Ordena los pasos en la secuencia lógica y, cuando sea pertinente, sugiere plazos/citas previas."
)

class PlannerAgent:
    def __init__(self, model_name: str = "openai/gpt-4o-mini", temperature: float = 0.1):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        ).with_structured_output(Plan)

    def plan(self, user_prompt: str, retrieval_context: str = "") -> Plan:
        ctx = f"\n\nContexto documental:\n{retrieval_context}" if retrieval_context else ""
        msgs = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Solicitud del ciudadano:\n{user_prompt}{ctx}")
        ]
        return self.llm.invoke(msgs)

if __name__ == "__main__":
    agent = PlannerAgent()
    demo = "Me mudo con mis dos hijos a otra comunidad. ¿Qué trámites debo seguir (padrón, colegio, sanidad)?"
    plan = agent.plan(demo)
    print(plan.json(indent=2, ensure_ascii=False))

