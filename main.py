from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime
import pytz

app = FastAPI()

@app.get("/")
async def mostrar_temperatura(request: Request):
    usuario = request.query_params.get("usuario", "Coplac")
    maquina = "PH 02"
    firebase_url = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(firebase_url, timeout=10)
            response.raise_for_status()

        temperatura_raw = response.json()

        if temperatura_raw is None:
            return JSONResponse(status_code=404, content={"erro": "Temperatura não encontrada no Firebase."})

        temperatura = round(float(temperatura_raw), 1)

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

    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"erro": f"Erro de conexão: {str(e)}"})
    except httpx.HTTPStatusError as e:
        return JSONResponse(status_code=500, content={"erro": f"Erro HTTP: {e.response.status_code}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Erro inesperado: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
