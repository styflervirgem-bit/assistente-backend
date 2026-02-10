import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Mensagem(BaseModel):
    mensagem: str

@app.post("/analisar")
async def analisar(dados: Mensagem):
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": dados.mensagem}
        ]
    )
    return {"resposta": resposta.choices[0].message.content}
