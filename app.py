"""Chatbot with document knowledge base (PDF, Word, Excel) and file generation.

Run:  uv run streamlit run app.py
"""

import streamlit as st

from engine import reply
from extractor import extract_text
from generator import generate_document

WELCOME = (
    "👋 Hi! I'm your back-office assistant. "
    "Upload a PDF, Word or Excel file in the sidebar to use it as reference, "
    "then ask me anything. I can also **create documents** — just ask!"
)

st.title("Agentic-Assistant 🤖📄")

# ── Sidebar: document uploader ──────────────────────────────────────────────
with st.sidebar:
    st.header("📁 Knowledge Base")
    st.info("Supported formats: **PDF** · **Word (.docx)** · **Excel (.xlsx)**")
    uploaded_files = st.file_uploader(
        "Upload a file to use as context",
        type=["pdf", "docx", "xlsx"],
        accept_multiple_files=True,
    )

    file_names = [f.name for f in uploaded_files] if uploaded_files else []

    if file_names != st.session_state.get("kb_file_names", []):
        if uploaded_files:
            with st.spinner("Reading documents…"):
                parts = []
                for f in uploaded_files:
                    try:
                        parts.append(f"=== {f.name} ===\n{extract_text(f)}")
                    except Exception as e:
                        parts.append(f"=== {f.name} ===\n[Error reading file: {e}]")
            st.session_state.kb_text = "\n\n".join(parts)
        else:
            st.session_state.kb_text = ""
        st.session_state.kb_file_names = file_names

    if file_names:
        st.success(f"{len(file_names)} file(s) loaded")
        for name in file_names:
            st.caption(f"• {name}")

# ── Chat history ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]

# downloads are stored separately to avoid passing bytes into the API history;
# each entry is a list of dicts so one message can have multiple files.
if "downloads" not in st.session_state:
    st.session_state.downloads = {}


def _render_message(m: dict, index: int) -> None:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        for j, d in enumerate(st.session_state.downloads.get(index, [])):
            st.download_button(
                label=f"⬇️ Download {d['filename']}",
                data=d["data"],
                file_name=d["filename"],
                mime=d["mime"],
                key=f"dl_{index}_{j}",
            )


for i, m in enumerate(st.session_state.messages):
    _render_message(m, i)

# ── Input box ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything, or ask me to create a Word / PDF / Excel file…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Only role + content go to the API — no extra keys (avoids serialisation errors)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
        if m["content"] != WELCOME
    ]
    kb = st.session_state.get("kb_text", "")

    msg_index = len(st.session_state.messages)
    files_for_msg = []
    answer = ""

    with st.status("Calling the model…", expanded=True) as status:

        # reply() is a generator: it yields (event_type, payload) tuples so we
        # can show live progress for every step of the agentic loop.
        for event_type, payload in reply(prompt, history, kb):

            if event_type == "step":
                st.write(payload)

            elif event_type == "tool":
                fmt = payload["format"].upper()
                st.write(f"Generating {fmt} document…")
                try:
                    data, filename, mime = generate_document(
                        payload["content"], payload["format"]
                    )
                    files_for_msg.append({"data": data, "filename": filename, "mime": mime})
                except Exception as e:
                    answer += f"\n\n⚠️ Could not generate {fmt} file: {e}"

            elif event_type == "done":
                answer = payload

        if files_for_msg:
            st.session_state.downloads[msg_index] = files_for_msg

        if not answer and files_for_msg:
            answer = "Here are the documents you requested."

        status.update(label="Done", state="complete", expanded=False)

    msg: dict = {"role": "assistant", "content": answer}
    st.session_state.messages.append(msg)
    _render_message(msg, msg_index)
