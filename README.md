# Step 1 — Prima chiamata al Generative Engine

Script Python minimale che mostra come connettersi al Generative Engine di Capgemini, inviare un messaggio e ricevere una risposta.

---

## Cosa fa

- Si collega all'endpoint OpenAI-compatible del Generative Engine
- Usa il modello `amazon.nova-lite-v1:0`
- Invia il messaggio "Ciao, presentati in una frase"
- Stampa la risposta in console
- Gestisce gli errori di timeout e connessione

## File

```
main.py       # script principale
config.py     # (assente in questo step, tutto in main.py)
```

---

## Come eseguire

1. Crea un file `.env` nella cartella del progetto:
   ```
   GEN_ENGINE_API_KEY=la-tua-chiave-api
   ```

2. Installa le dipendenze:
   ```bash
   uv sync
   ```

3. Esegui:
   ```bash
   uv run python main.py
   ```

---

## Come è stato creato

Generato con `prompt_0.md` — disponibile nel branch `main`.

Per vedere il passo successivo: `git checkout simple-chatbot`
