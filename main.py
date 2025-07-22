from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/")
async def mostrar_temperatura(request: Request):
    usuario = request.query_params.get("usuario", "Coplac")  # Padrão = Coplac
    maquina = "PH 02"
    firebase_url = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"

    try:
        response = requests.get(firebase_url)
        response.raise_for_status()
        temperatura_raw = response.json()

        if temperatura_raw is None:
            return JSONResponse(status_code=404, content={"erro": "Temperatura não encontrada no Firebase."})

        temperatura = round(float(temperatura_raw), 1)

        # Hora em tempo real com fuso horário do Brasil
        fuso = pytz.timezone("America/Sao_Paulo")
        agora = datetime.now(fuso)
        data_atual = agora.strftime("%d/%m/%Y")
        hora_atual = agora.strftime("%H:%M:%S")

        return {
            "Temperatura (°C)": f"{temperatura} ºC",
            "Usuário": usuario,
            "Máquina": maquina,
            "Data": data_atual,
            "Hora": hora_atual
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Falha ao acessar o Firebase: {str(e)}"})
