from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "API funcionando!"}

@app.get("/temperatura")
def get_temperatura():
    firebase_url = "https://projetotemperaturaesp32-52b7d-default-rtdb.firebaseio.com/temperatura_ao_vivo.json"
    try:
        response = requests.get(firebase_url)
        response.raise_for_status()
        temperatura = response.json()
        if temperatura is None:
            return {"erro": "Temperatura não disponível"}
        temperatura = round(float(temperatura), 1)
        return {"temperatura": temperatura}
    except Exception as e:
        return {"erro": f"Falha ao acessar Firebase: {str(e)}"}
