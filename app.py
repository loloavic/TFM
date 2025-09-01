# app.py  (en la raíz del repo)
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Agentes (manteniendo tu estructura)
from agents.retrieval_agent import RetrievalAgent
from agents.planner_agent import PlannerAgent
from agents.verifier_agent import VerifierAgent
from agents.executor_agent import ExecutorAgent

# Opcional: webhook de n8n para ejecutar acciones
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")  # e.g. https://tu-n8n.com/webhook/tfm/acciones
N8N_SECRET = os.getenv("N8N_SECRET")            # si validas un header secreto en n8n

class InPayload(BaseModel):
    user_prompt: str

app = FastAPI(title="TFM Backend — Rutas Administrativas")

# CORS (en desarrollo deja *; en prod limita a tu dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/plan")
def make_plan(p: InPayload):
    try:
        # 1) Recuperación (RAG) — lee documentos de rag_engine/document_store
        retriever = RetrievalAgent()
        ctx = retriever.get_context(p.user_prompt)

        # 2) Planificación con LLM
        planner = PlannerAgent()
        plan = planner.plan(p.user_prompt, retrieval_context=ctx)

        # 3) Verificación (reglas simples)
        verifier = VerifierAgent()
        issues = verifier.verify(plan, p.user_prompt)

        # 4) Acciones “ejecutables” para n8n
        executor = ExecutorAgent()
        actions = executor.to_actions(plan)

        # 5) (Opcional) disparamos n8n con plan+acciones
        if N8N_WEBHOOK_URL:
            headers = {"Content-Type": "application/json"}
            if N8N_SECRET:
                headers["X-TFM-Token"] = N8N_SECRET
            try:
                requests.post(N8N_WEBHOOK_URL, json={"plan": plan.dict(), "actions": actions},
                              headers=headers, timeout=20)
            except Exception as e:
                # loguea, pero no rompas la respuesta al usuario
                print("Error llamando a n8n:", e)

        return {"plan": plan.dict(), "issues": issues, "actions": actions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
