# agentes/classifier_agent.py (versión compatible con LangChain 0.1/0.2)
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

class ClassifierAgent:
    def __init__(self, model_name="openai/gpt-4o-mini", temperature=0.2):
        # Opción A: pasar la clave OpenRouter directamente
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )
        self.prompt = PromptTemplate.from_template(
            "Clasifica el siguiente mensaje en una de estas categorías:\n"
            "1. Mudanza con hijos\n"
            "2. Mudanza sin hijos\n"
            "3. Cambio de comunidad por trabajo\n"
            "4. Cambio de comunidad por motivos generales\n"
            "5. Otro\n\n"
            "Mensaje: {input}\n\n"
            "Categoría (devuelve solo el nombre exacto de la categoría):"
        )

    def classify(self, user_input: str) -> str:
        prompt = self.prompt.format(input=user_input)
        # En LangChain moderno, .invoke() sobre una lista de mensajes
        resp = self.llm.invoke([HumanMessage(content=prompt)])
        return resp.content.strip()

if __name__ == "__main__":
    agent = ClassifierAgent()
    test = "Me estoy mudando con mi familia y mis dos hijos a otra ciudad por trabajo. ¿Qué debo hacer con la escuela y el padrón?"
    print("Categoría detectada:", agent.classify(test))

