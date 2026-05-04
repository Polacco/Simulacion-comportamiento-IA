import os
from dotenv import load_dotenv
from agentes import AgenteOficina
from prompts import PROMPT_JORGE

load_dotenv() 

def simular_oficina(): #test
    api_key = os.getenv("GROQ_API_KEY")
    print(f"DEBUG: La clave cargada empieza con: {api_key[:10] if api_key else 'NADA'}")

    if not api_key:
        print("ERROR: No se encontró la GROQ_API_KEY. Revisá el archivo .env")
        return

    jorge = AgenteOficina("Jorge", PROMPT_JORGE, (1, 1))
    
    estado_del_mundo = "Lunes 9:00 AM. Jorge entra a la oficina eufórico con una idea."
    
    print(f"--- Turno de {jorge.nombre} ---")
    decision = jorge.decidir_accion(estado_del_mundo)
    print(decision)

if __name__ == "__main__":
    simular_oficina()