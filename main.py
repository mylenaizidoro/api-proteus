from fastapi import FastAPI
import requests
from datetime import datetime
import pytz

app = FastAPI()

# URLs do Firebase
URL_ATUAL = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"
URL_HISTORICO = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/historico_temperaturas.json"

@app.get("/")
def registrar_temperatura():
    try:
        # Buscar temperatura atual
        response = requests.get(URL_ATUAL)
        response.raise_for_status()
        temperatura_atual = response.json()

        if temperatura_atual is None:
            return {"erro": "Temperatura nao disponivel"}

        temperatura_atual = round(float(temperatura_atual), 1)

        # Buscar historico
        historico_resp = requests.get(URL_HISTORICO)
        historico = historico_resp.json()

        ultima_temp = None
        if historico:
            ultimos = list(historico.values())
            ultima_str = ultimos[-1].get("temperatura_celsius", "").replace(" C", "").replace(",", ".")
            if ultima_str:
                try:
                    ultima_temp = float(ultima_str)
                except:
                    ultima_temp = None

        # Registrar apenas se mudou
        if ultima_temp is None or temperatura_atual != ultima_temp:
            fuso = pytz.timezone("America/Sao_Paulo")
            agora = datetime.now(fuso)
            data = agora.strftime("%d/%m/%Y")
            hora = agora.strftime("%H:%M:%S")

            leitura = {
                "temperatura_celsius": f"{temperatura_atual} C",
                "usuario": "Coplac Curitiba",
                "maquina": "PH 02",
                "data": data,
                "hora": hora
            }

            requests.post(URL_HISTORICO, json=leitura)

            return leitura

        else:
            return {
                "mensagem": "Temperatura sem mudanca",
                "temperatura_celsius": f"{temperatura_atual} C"
            }

    except Exception as e:
        return {"erro": str(e)}

