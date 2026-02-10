from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mensagem(BaseModel):
    mensagem: str

@app.post("/analisar")
async def analisar(dados: Mensagem):
    texto = dados.mensagem

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um especialista em responder conversas de forma natural, confiante e respeitosa."},
            {"role": "user", "content": texto}
        ],
        temperature=0.7,
    )

    return {
        "resposta": resposta.choices[0].message.content
    }
