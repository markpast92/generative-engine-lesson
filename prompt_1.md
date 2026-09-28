Trasforma questo progetto in un chatbot Streamlit completo.

[inserire il main di April]

Genera tutti i file completi.

Struttura:

app.py
config.py
engine.py

Requisiti:

config.py:
- legge GEN_ENGINE_API_KEY da .env
- contiene MODEL="amazon.nova-lite-v1:0"
- contiene SYSTEM_PROMPT
- inizializza il client

engine.py:
- espone reply(message, history)
- mantiene la conversazione usando tutta la history

app.py:
- interfaccia Streamlit
- cronologia chat
- chat_input
- visualizzazione markdown

Mantieni il codice semplice.
Non usare classi.
Non usare framework aggiuntivi.
Genera il contenuto completo di tutti i file.

utilizza uv add e nome della libreria per installare i pacchetti

Output: genera solo i file completi, verificati, testati, senza errori di import, pronti all'esecuzione immediata senza spiegazioni aggiuntive.