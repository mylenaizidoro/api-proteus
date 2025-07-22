from fastapi import FastAPI
import requests
from datetime import datetime
import pytz

app = FastAPI()

# Configuração
URL_FIREBASE_ATUAL = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"
URL_FIREBASE_HISTORICO = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/historico_temperaturas.json"

@app.get("/")
def registrar_temperatura():
    try:
        # Lê temperatura atual do sensor no Firebase
        response = requests.get(URL_FIREBASE_ATUAL)
        response.raise_for_status()
        temperatura_atual = response.json()

        if temperatura_atual is None:
            return {"erro": "Temperatura não disponível"}

        temperatura_atual = round(float(temperatura_atual), 1)

        # Busca o último valor salvo no histórico
        historico_resp = requests.get(URL_FIREBASE_HISTORICO)
        historico = historico_resp.json()

        ultima_temp = None
        if historico:
            ultimos_registros = list(historico.values())
            ultima_temp_raw = ultimos_registros[-1]["Temperatura (°C)"]
            ultima_temp = float(ultima_temp_raw.replace(" ºC", "").replace(",", "."))

        # Se mudou, salva no histórico
        if ultima_temp is None or temperatura_atual != ultima_temp:
            fuso = pytz.timezone("America/Sao_Paulo")
            agora = datetime.now(fuso)
            data = agora.strftime("%d/%m/%Y")
            hora = agora.strftime("%H:%M:%S")

            leitura = {
                "Temperatura (°C)": f"{temperatura_atual} ºC",
                "Usuário": "Coplac Curitiba",
                "Máquina": "PH 02",
                "Data": data,
                "Hora": hora
            }

            requests.post(URL_FIREBASE_HISTORICO, json=leitura)

            return {
                "mensagem": "Nova temperatura registrada!",
                "leitura": leitura
            }

        else:
            return {
                "mensagem": "Sem variação. Temperatura não registrada novamente.",
                "temperatura_igual": f"{temperatura_atual} ºC"
            }

    except Exception as e:
        return {"erro": f"Erro ao registrar temperatura: {str(e)}"}
