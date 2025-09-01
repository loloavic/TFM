# agentes/executor_agent.py
# Serializa el plan a una lista de acciones que nuestro workflow de n8n pueda iterar

from typing import List, Dict, Any
from agents.planner_agent import Plan

class ExecutorAgent:
    def to_actions(self, plan: Plan) -> List[Dict[str, Any]]:
        actions = []
        for s in plan.steps:
            actions.append({
                "type": "email_summary",
                "body": f"- Paso: {s.titulo}\n- Documentos: {', '.join(s.documentos)}",
            })
            if s.formulario:
                actions.append({
                    "type": "link",
                    "url": s.formulario,
                    "label": f"Formulario: {s.titulo}"
                })
        if plan.recomendaciones:
            actions.append({
                "type": "notes",
                "items": plan.recomendaciones
            })
        return actions
