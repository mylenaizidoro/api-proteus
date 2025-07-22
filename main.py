from fastapi import FastAPI, Request
import requests
from datetime import datetime

app = FastAPI()

@app.get("/")
def get_temperatura(request: Request):
    firebase_url = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"
    
    try:
        # Lê temperatura do Firebase
        response = requests.get(firebase_url)
        response.raise_for_status()
        temperatura = response.json()
        
        # Verifica valor
        if temperatura is None:
            return {"erro": "Temperatura não disponível"}
        
        temperatura = round(float(temperatura), 1)
        
        if temperatura > 100 or temperatura < -20:
            return {"erro": f"Temperatura fora do intervalo aceitável: {temperatura} ºC"}

        # Dados formatados
        data = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M")
        usuario = request.query_params.get("usuario", "Desconhecido")
        maquina = "PH 02"

        return {
            "Temperatura (°C)": f"{temperatura} ºC",
            "Usuário": usuario,
            "Máquina": maquina,
            "Data": data,
            "Hora": hora
        }

    except Exception as e:
        return {"erro": f"Falha ao acessar Firebase: {str(e)}"}
