Agisci come un Senior Python Engineer.

Estendi il progetto esistente aggiungendo il ciclo agentico e la generazione di documenti.

Ecco i file attuali del progetto:

[inserire qui il contenuto completo di config.py, extractor.py, engine.py, app.py]

La nuova struttura sarà di 5 file:

- config.py (da aggiornare)
- extractor.py (da aggiornare)
- engine.py (da riscrivere completamente)
- generator.py (nuovo file)
- app.py (da riscrivere completamente)

---

config.py — modifiche richieste:
- mantieni URL, chiave API e system prompt esistenti
- aggiungi la variabile: MAX_TOKENS = 8192
- sostituisci la funzione get_client() con una variabile a livello di modulo:
  client = OpenAI(base_url=..., api_key=...)
- usa il modello: MODEL = "anthropic.claude-sonnet-4-6"

extractor.py — modifiche richieste:
- cambia la firma della funzione principale in: extract_text(file)
  dove file è l'oggetto UploadedFile di Streamlit (ha attributo .name)
- per i PDF usa pypdf: from pypdf import PdfReader
- per gli Excel usa pandas: import pandas as pd, poi pd.read_excel(file, sheet_name=None)
- per i Word usa python-docx: import docx

generator.py — nuovo file da creare:
- genera documenti in memoria senza mai salvare file su disco (usa BytesIO)
- funzione principale: generate_document(text, fmt) che restituisce (bytes, filename, mime_type)
- fmt può essere: "pdf", "docx", "xlsx"
- per PDF usa fpdf: from fpdf import FPDF
- per Word usa python-docx: import docx
- per Excel usa openpyxl: import openpyxl
- nel testo, le righe che iniziano con "# " sono intestazioni
- per Excel, le colonne di ogni riga sono separate dal carattere "|"

engine.py — riscrivere completamente con queste regole:
- la funzione reply(message, history, knowledge_base) deve essere un generatore Python
  (usa yield invece di return, il chiamante farà un loop: for event_type, payload in reply(...))
- produce solo questi tre tipi di eventi:
  - ("step", testo): per mostrare messaggi di avanzamento all'utente
  - ("tool", {"format": "pdf|docx|xlsx", "content": "..."}): quando il modello vuole creare un documento
  - ("done", testo): messaggio finale del modello, segna la fine del loop
- definisce un tool OpenAI chiamato create_document con i parametri:
  - format: stringa enum con valori "docx", "pdf", "xlsx"
  - content: stringa con il contenuto completo del documento da creare
- usa OpenAI tool calling: passa tools=[...] nella chiamata al modello
- IMPORTANTE — iniezione del system prompt:
  Il Generative Engine non accetta il ruolo "system" nei messaggi.
  Il system prompt va inserito come PRIMO scambio della conversazione in questo modo:
    messaggio 1: {"role": "user", "content": <testo del system prompt>}
    messaggio 2: {"role": "assistant", "content": "Understood. How can I help you?"}
  Dopodiche si aggiungono i messaggi reali dell'utente.
- quando il modello chiama un tool, aggiungi alla lista dei messaggi:
  1. il messaggio dell'assistant che contiene tool_calls
  2. il risultato del tool con role "tool" (NON "user"), con tool_call_id corrispondente
- massimo 5 iterazioni nel loop prima di fermarsi
- importa client e MAX_TOKENS direttamente da config (non usare get_client())
- gestisci il caso in cui il modello non supporta tool calling: cattura BadRequestError
  e PermissionDeniedError, fai una chiamata senza tools e restituisci la risposta testuale

app.py — riscrivere completamente con queste regole:
- interfaccia Streamlit con titolo "Agentic-Assistant"
- sidebar con file_uploader per PDF, DOCX, XLSX (accept_multiple_files=True)
- salva il testo estratto in st.session_state.kb_text
  e rileggi i file solo quando cambia la lista dei file caricati (confronta i nomi)
- cronologia chat in st.session_state.messages (lista di dict con role e content)
- salva i file generati in st.session_state.downloads
  (dizionario da indice del messaggio a lista di file, ogni file è dict con data, filename, mime)
- non includere mai i bytes dei file nei messaggi inviati all'API
- per ogni risposta dell'utente, chiama reply() e fai un loop sugli eventi:
  - "step": mostra il testo in un pannello st.status
  - "tool": chiama generate_document() e aggiungi il file alla lista downloads
  - "done": salva il testo come risposta finale dell'assistant
- mostra i pulsanti download_button sotto il messaggio corrispondente

Pacchetti da installare con uv add:
streamlit openai python-dotenv python-docx pypdf fpdf openpyxl

Regole generali:
- usa BytesIO, non salvare mai file su disco
- codice semplice e leggibile, senza classi inutili
- nessun errore di sintassi
- pronto da eseguire con: uv run streamlit run app.py

Output: genera solo i file completi, verificati, testati, senza errori di import, pronti all'esecuzione immediata, senza spiegazioni aggiuntive.
