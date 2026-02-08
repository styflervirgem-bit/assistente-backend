from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

@app.post("/analisar")
async def analisar(file: UploadFile = File(...)):
    # OCR
    ocr_api_key = os.getenv("OCR_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    ocr_response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"file": await file.read()},
        data={
            "apikey": ocr_api_key,
            "language": "por"
        }
    )

    texto = ocr_response.json()["ParsedResults"][0]["ParsedText"]

    # OpenAI
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Você é um assistente de comunicação respeitoso.

Analise a conversa abaixo e gere:
1. Sentimento
2. Interesse
3. Intenção
4. 3 sugestões de resposta:
- Leve
- Divertida
- Direta

Conversa:
{texto}
"""

    ia_response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    resposta = ia_response.json()["choices"][0]["message"]["content"]
    return {"resultado": resposta}
