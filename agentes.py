import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompts import SYSTEM_PROMPT_BASE

class AgenteOficina:
    def __init__(self, nombre, personalidad_prompt, coordenadas_inicio):
        self.nombre = nombre
        self.personalidad = personalidad_prompt
        self.posicion = coordenadas_inicio
        self.memoria_reciente = []
        
        # configuramos el modelo
        self.llm = ChatGroq(
            temperature=0.8, # un poco de aleatoriedad
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def decidir_accion(self, estado_mundo):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT_BASE + self.personalidad),
            ("human", "Estado del mundo actual: {estado_mundo}\n¿Cuál es tu siguiente movimiento?")
        ])
        
        chain = prompt_template | self.llm
        respuesta = chain.invoke({"estado_mundo": estado_mundo})
        return respuesta.content