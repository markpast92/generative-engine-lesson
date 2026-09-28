"""Configuration: API key, model, client and system prompt for the Generative Engine."""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load the .env file so the API key is available as an environment variable
load_dotenv()

# The client talks to Capgemini's Generative Engine (OpenAI-compatible API)
client = OpenAI(
    base_url="https://openai.generative.engine.capgemini.com/v1",
    api_key=os.getenv("GEN_ENGINE_API_KEY"),
)

# The model is the chatbot's "brain": change this line to switch model
# MODEL = "amazon.nova-lite-v1:0"   # does not support tool calling
MODEL = "anthropic.claude-sonnet-4-6"

# Max tokens for the model response; increase if replies get cut off (finish_reason='length')
MAX_TOKENS = 8192

# The system prompt defines the assistant's scope, so users know what it covers
SYSTEM_PROMPT = (
    "You are a helpful back-office assistant for Capgemini employees. "
    "You help with documents, invoices, spreadsheets and internal processes. "
    "Be concise and friendly, use Markdown when useful, and always reply in the "
    "user's language. If a request is outside this scope, say so briefly."
)
