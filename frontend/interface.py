# frontend/interface.py
import os, requests, gradio as gr

# Si el backend está local: http://localhost:8000/plan
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/plan")

def generar(prompt: str):
    if not prompt or not prompt.strip():
        return "Por favor, describe tu situación en el cuadro de texto."
    r = requests.post(BACKEND_URL, json={"user_prompt": prompt}, timeout=60)
    r.raise_for_status()
    data = r.json()

    steps = data["plan"].get("steps", [])
    recs = data["plan"].get("recomendaciones", [])
    issues = data.get("issues", [])

    md = "### Ruta propuesta\n"
    if not steps:
        md += "_No se generaron pasos. Revisa la entrada._\n"
    else:
        for i, s in enumerate(steps, 1):
            docs = ", ".join(s.get("documentos", [])) or "—"
            resp = s.get("responsable") or "—"
            form = s.get("formulario") or "—"
            md += f"{i}. **{s['titulo']}**  \n   - Documentos: {docs}  \n   - Responsable: {resp}  \n   - Formulario: {form}\n"

    if recs:
        md += "\n**Recomendaciones:** " + "; ".join(recs) + "\n"
    md += "\n**Posibles faltas:**\n" + ("\n".join([f"- {x}" for x in issues]) if issues else "Ninguna")

    return md

demo = gr.Interface(
    fn=generar,
    inputs=gr.Textbox(lines=5, label="Describe tu situación (ej.: 'Me mudo con hijos en edad escolar')"),
    outputs=gr.Markdown(),
    title="Asistente de Rutas Administrativas",
    description="Genera una ruta de trámites personalizada y (opcionalmente) dispara automatizaciones en n8n."
)

if __name__ == "__main__":
    # Si el backend está en VPS, define la URL:
    # PowerShell:  $Env:BACKEND_URL="https://TU_BACKEND/plan"
    demo.launch(server_name="0.0.0.0", server_port=7860)
