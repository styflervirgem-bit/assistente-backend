from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Mensagem(BaseModel):
    mensagem: str

@app.post("/analisar")
async def analisar(dados: Mensagem):
    texto = dados.mensagem
    return {"resposta": f"Você disse: {texto}"}
