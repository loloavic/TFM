# agentes/retrieval_agent.py
# Devuelve un contexto concatenado de archivos de texto ya extraidos

from pathlib import Path

class RetrievalAgent:
    def __init__(self, store_dir: str = "rag_engine/document_store"):
        self.store = Path(store_dir)

    def get_context(self, query: str, max_chars: int = 4000) -> str:
        # Stub: concatena texto plano de .txt (puedes preprocesar PDFs a .txt)
        chunks = []
        for p in self.store.glob("**/*.txt"):
            try:
                t = p.read_text(encoding="utf-8")
                chunks.append(t)
            except Exception:
                continue
            if sum(len(c) for c in chunks) > max_chars:
                break
        return "\n\n".join(chunks)[:max_chars]
