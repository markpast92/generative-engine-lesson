import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# modello semplice, meno costoso ma più impreciso
# MODEL = "amazon.nova-lite-v1:0"

# modello più complesso, più costoso, ma più preciso
MODEL = "anthropic.claude-sonnet-4-6"

SYSTEM_PROMPT = """Sei un assistente utile e amichevole. 
Rispondi in modo chiaro e conciso.
Mantieni un tono professionale ma cordiale."""

def get_client():
    return OpenAI(
        base_url="https://openai.generative.engine.capgemini.com/v1",
        api_key=os.environ.get("GEN_ENGINE_API_KEY"),
        timeout=60.0,
    )