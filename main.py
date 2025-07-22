from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from datetime import datetime

app = FastAPI()

@app.get("/")
async def mostrar_temperatura(request: Request):
    # Valor padrão: Coplac Curitiba
    usuario = request.query_params.get("usuario", "Coplac Curitiba")
    maquina = "PH 02"
    firebase_url = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"

    try:
        response = requests.get(firebase_url)
        response.raise_for_status()
        temperatura_raw = response.json()

        if temperatura_raw is None:
            return JSONResponse(status_code=404, content={"erro": "Temperatura não encontrada no Firebase."})

        temperatura = round(float(temperatura_raw), 1)
        data_atual = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%H:%M")

        return {
            "Temperatura (°C)": f"{temperatura} ºC",
            "Usuário": usuario,
            "Máquina": maquina,
            "Data": data_atual,
            "Hora": hora_atual
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Falha ao acessar o Firebase: {str(e)}"})
