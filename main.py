import os
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIStatusError, APITimeoutError

# Carica le variabili dal file .env
load_dotenv()

# Client OpenAI-compatible con endpoint Generative Engine (US)
client = OpenAI(
    base_url="https://openai.generative.engine.capgemini.com/v1",
    api_key=os.environ["GEN_ENGINE_API_KEY"],
    timeout=60.0,
)

try:
    response = client.chat.completions.create(
        model="amazon.nova-lite-v1:0",
        messages=[
            {"role": "user", "content": "Ciao, presentati in una frase."}
        ],
        max_completion_tokens=256,
    )
    print(response.choices[0].message.content)

except APITimeoutError:
    print("Richiesta scaduta (timeout). Riprova.")
except APIConnectionError as exc:
    print(f"Impossibile contattare Generative Engine: {exc}")
except APIStatusError as exc:
    print(f"Errore HTTP {exc.status_code}: {exc.response.text}")