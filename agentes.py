import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompts import SYSTEM_PROMPT_BASE

class AgenteOficina:
    def __init__(self, nombre, personalidad_prompt, coordenadas_inicio):
        self.nombre = nombre
        self.personalidad = personalidad_prompt
        self.posicion = coordenadas_inicio
        self.memoria_reciente = []
        
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def decidir_accion(self, estado_mundo):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT_BASE + self.personalidad),
            ("human", f"Historial reciente:\n{self.memoria_reciente}\n\nEstado del mundo: {estado_mundo}\n¿Qué haces?")
        ])
        
        chain = prompt_template | self.llm
        raw_response = chain.invoke({"estado_mundo": estado_mundo}).content
        
        try:
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            # guardamos en memoria
                self.memoria_reciente.append(f"Acción: {data.get('accion')}, Dijo: {data.get('dialogo')}")
                if len(self.memoria_reciente) > 5: self.memoria_reciente.pop(0)
                return data
            return {"error": "No se pudo parsear"}
        except Exception as e:
            return {"error": str(e)}