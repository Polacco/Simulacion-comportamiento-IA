# main.py
import os
import time
import asyncio
import uvicorn # Lo movemos arriba
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

print("--- 🏁 Iniciando script main.py ---")

load_dotenv()
print(f"DEBUG: API Key cargada: {'SÍ' if os.getenv('GROQ_API_KEY') else 'NO'}")

from agentes import AgenteOficina
from prompts import PROMPT_JORGE, PROMPT_PEDRO, PROMPT_LUCAS, PROMPT_JUAN, PROMPT_JULIA
from mapa import obtener_descripcion_mapa

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 🚀 Servidor FastAPI arrancando ---")
    task = asyncio.create_task(loop_simulacion())
    yield
    print("--- 🛑 Apagando task de simulación ---")
    task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("--- 👥 Inicializando equipo de agentes ---")
equipo = [
    AgenteOficina("Jorge", PROMPT_JORGE, (1, 1)),
    AgenteOficina("Pedro", PROMPT_PEDRO, (10, 1)),
    AgenteOficina("Lucas", PROMPT_LUCAS, (1, 10)),
    AgenteOficina("Juan", PROMPT_JUAN, (3, 1)),
    AgenteOficina("Julia", PROMPT_JULIA, (10, 10))
]

estado_del_mundo = "Mañana tranquila en la oficina. Jorge está por anunciar su idea del collar con IA."

@app.get("/estado")
async def get_estado():
    return {
        "agentes": [
            {
                "nombre": a.nombre,
                "x": a.posicion[0],
                "y": a.posicion[1],
                "mensaje": a.ultimo_mensaje,
                "emoji": a.ultimo_emoji
            } for a in equipo
        ],
        "mundo": estado_del_mundo
    }

async def loop_simulacion():
    global estado_del_mundo
    mapa_desc = obtener_descripcion_mapa()
    print("--- 🧠 Loop de simulación iniciado ---")
    
    while True:
        try:
            for agente in equipo:
                print(f"🤔 {agente.nombre} pensando turno...")
                contexto_extra = "\nREGLA: Si no estás cerca de alguien, CAMINA hacia su lugar para hablar."
                decision = agente.decidir_accion(estado_del_mundo + contexto_extra, mapa_desc)
                
                if "dialogo" in decision and decision["dialogo"]:
                    estado_del_mundo += f"\n{agente.nombre}: {decision['dialogo']}"
                
                await asyncio.sleep(4)
            
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error en el loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    print("--- 📡 Llamando a uvicorn.run ---")
    uvicorn.run(app, host="0.0.0.0", port=8000)