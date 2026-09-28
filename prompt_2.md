Estendi il progetto mantenendo intatti i file esistenti.

[inserire i tre file prodotti in precedenza]

Nuova struttura:

app.py
config.py
engine.py
extractor.py

Requisiti:

- upload PDF DOCX XLSX
- sidebar Streamlit
- estrazione testo
- knowledge_base passata a reply()
- nessuna modifica architetturale inutile
- genera il contenuto completo di tutti i file modificati

utilizza uv add e nome della libreria per installare i pacchetti

Mostriamo la differenza tra questi due modelli, prima attivami il primo e poi mi provo il secondo.
# modello semplice, meno costoso ma più impreciso
MODEL = "amazon.nova-lite-v1:0"

# modello più complesso, più costoso, ma più preciso
# MODEL = "anthropic.claude-sonnet-4-6"

Output: genera solo i file completi, verificati, testati, senza errori di import, pronti all'esecuzione immediata senza spiegazioni aggiuntive.