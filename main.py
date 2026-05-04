import os
import time
from dotenv import load_dotenv
from agentes import AgenteOficina
from prompts import PROMPT_JORGE, PROMPT_PEDRO, PROMPT_LUCAS, PROMPT_JUAN, PROMPT_JULIA

load_dotenv()

def simular_oficina():
    equipo = [
        AgenteOficina("Jorge", PROMPT_JORGE, (1, 1)),
        AgenteOficina("Pedro", PROMPT_PEDRO, (10, 1)),
        AgenteOficina("Lucas", PROMPT_LUCAS, (1, 10)),
        AgenteOficina("Juan", PROMPT_JUAN, (3, 1)),
        AgenteOficina("Julia", PROMPT_JULIA, (10, 10))
    ]
    
    estado_del_mundo = "Jorge se para en medio de la oficina y grita: '¡Equipo, dejen todo! Vamos a fabricar un collar con IA que te dice cuándo tenés hambre. ¡Es el futuro!'"
    print(f"🌍 EVENTO GLOBAL: {estado_del_mundo}\n")

    # ciclo de Reacción
    for agente in equipo:
        print(f"--- {agente.nombre} está pensando... ---")
        decision = agente.decidir_accion(estado_del_mundo)
        
        # mostramos las reacciones del agente
        emoji = decision.get('emoji', '🤔')
        dialogo = decision.get('dialogo', '...')
        pensamiento = decision.get('pensamiento_interno', '...')
        
        print(f"{emoji} {agente.nombre}: \"{dialogo}\"")
        print(f"💭 (Pensamiento: {pensamiento})\n")
        
        if dialogo:
            estado_del_mundo += f"\n{agente.nombre} dijo: '{dialogo}'"
        
        time.sleep(1) # para no saturar la API

if __name__ == "__main__":
    simular_oficina()