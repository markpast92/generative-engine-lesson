# Live Lesson — Punto di Partenza

Questo branch è il punto di partenza per la lezione live. Il progetto è vuoto: puoi iniziare a scrivere il codice da zero seguendo i prompt nel branch `main`.

---

## Come si usa durante la lezione

1. Crea un file `.env` con la tua chiave API:
   ```
   GEN_ENGINE_API_KEY=la-tua-chiave-api
   ```

2. Segui i prompt nel branch `main` step by step:
   - `prompt_0.md` → crea `main.py` (prima chiamata API)
   - `prompt_1.md` → aggiungi Streamlit (chatbot)
   - `prompt_2.md` → aggiungi upload documenti
   - `prompt_3.md` → aggiungi agentic loop e generazione documenti

3. Installa i pacchetti man mano che li aggiungi:
   ```bash
   uv add openai python-dotenv
   uv add streamlit
   uv add pypdf python-docx openpyxl fpdf
   ```

4. Avvia l'app:
   ```bash
   uv run streamlit run app.py
   ```

---

Per vedere il risultato finale: `git checkout agent-with-tools`
Per i prompt e la spiegazione completa: `git checkout main`
