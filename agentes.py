import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompts import SYSTEM_PROMPT_BASE
from mapa import LUGARES

class AgenteOficina:
    def __init__(self, nombre, personalidad_prompt, coordenadas_inicio):
        self.nombre = nombre
        self.personalidad = personalidad_prompt
        self.posicion = coordenadas_inicio
        self.memoria_reciente = []
        self.ultimo_mensaje = ""
        self.ultimo_emoji = "😐"
        
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def decidir_accion(self, estado_mundo, mapa_descripcion):
        sistema_texto = SYSTEM_PROMPT_BASE + self.personalidad + "\n" + mapa_descripcion
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", sistema_texto),
            ("human", "Tu posición actual: {posicion}\nHistorial: {historial}\nEstado del mundo: {estado_mundo}\n¿Qué haces?")
        ])
        
        chain = prompt_template | self.llm
        
        try:
            respuesta = chain.invoke({
                "posicion": self.posicion,
                "historial": self.memoria_reciente,
                "estado_mundo": estado_mundo
            })
            
            raw_response = respuesta.content
            
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                # logica de movimiento
                accion = data.get("accion")
                destino = data.get("destino")

                if accion == "CAMINAR" and destino in LUGARES:
                    self.posicion = LUGARES[destino]
                    print(f"📍 {self.nombre} caminó hacia {destino} {self.posicion}")
                
                self.ultimo_mensaje = data.get("dialogo", "")
                self.ultimo_emoji = data.get("emoji", "😐")
                
                resumen = f"Acción: {accion}"
                if dialogo := data.get("dialogo"):
                    resumen += f", Dijo: '{dialogo}'"
                if destino:
                    resumen += f", Destino: {destino}"
                
                self.memoria_reciente.append(resumen)
                if len(self.memoria_reciente) > 5: 
                    self.memoria_reciente.pop(0)
                
                return data
            
            return {"error": "No se encontró JSON válido", "raw": raw_response}
            
        except Exception as e:
            print(f"❌ Error en decidir_accion de {self.nombre}: {e}")
            return {"error": str(e)}