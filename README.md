# Proyecto: Agente Clasificador de Casos de Vida

Este proyecto implementa un agente de IA basado en LLM para **clasificar prompts ciudadanos** en distintas categorías de casos de vida,
como "mudanza con hijos", "mudanza sin hijos", "cambio de comunidad por trabajo" u "otros".

## Estructura

- `classifier_agent.py`: código del agente clasificador.
- `prompts_simulados.csv`: dataset de prueba con mensajes simulados y la categoría esperada.
- `validacion_classifier_agent.ipynb`: notebook para probar el clasificador y evaluar su rendimiento.
- `requirements.txt`: dependencias mínimas del proyecto.

## Instalación

1. Crea y activa un entorno virtual (recomendado con `venv` o `conda`).
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Exporta tu clave de API de OpenRouter:
   ```bash
   export OPENROUTER_API_KEY="tu_api_key_aqui"
   ```

2. Ejecuta el notebook de validación en Jupyter Lab:
   ```bash
   jupyter lab validacion_classifier_agent.ipynb
   ```

3. Observa los resultados de clasificación y la métrica de accuracy.

## Notas

- El agente está configurado por defecto para usar el modelo `gpt-3.5-turbo` vía OpenRouter, 
  pero se puede ajustar a otros modelos (ej. `gpt-4`, `mistral-7b`).
- Este es un prototipo inicial como parte del TFM para orquestar agentes inteligentes con LangGraph y automatización No-Code (n8n).
