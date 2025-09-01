# agentes/verifier_agent.py
# Reglas para detectar omisiones tipicas

from typing import List
from agents.planner_agent import Plan

class VerifierAgent:
    def verify(self, plan: Plan, raw_prompt: str) -> List[str]:
        issues = []
        if not plan.steps:
            issues.append("El plan no contiene pasos.")
            return issues
        text = raw_prompt.lower()
        titles = " ".join(s.titulo.lower() for s in plan.steps)

        if "muda" in text or "traslad" in text:
            if "empadron" not in titles:
                issues.append("Falta un paso de empadronamiento.")

        if ("hijo" in text or "escolar" in text) and "escolar" not in titles:
            issues.append("Falta un paso de solicitud de plaza escolar.")

        return issues
