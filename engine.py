from config import get_client, MODEL, SYSTEM_PROMPT
from openai import APITimeoutError, APIConnectionError, APIStatusError

def reply(message, history):
    client = get_client()
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_completion_tokens=512,
        )
        return response.choices[0].message.content
    
    except APITimeoutError:
        return "⏱️ Richiesta scaduta. Riprova."
    except APIConnectionError as exc:
        return f"❌ Errore di connessione: {exc}"
    except APIStatusError as exc:
        return f"❌ Errore HTTP {exc.status_code}: {exc.response.text}"