"""Chat logic: the function that talks to the model."""

import json

from openai import BadRequestError, PermissionDeniedError

from config import MAX_TOKENS, MODEL, SYSTEM_PROMPT, client

_DOCUMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "create_document",
        "description": (
            "Create a downloadable document with the content the user requested. "
            "Call this whenever the user asks to produce a file (Word, PDF or Excel)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["docx", "pdf", "xlsx"],
                    "description": "File format: docx (Word), pdf, or xlsx (Excel).",
                },
                "content": {
                    "type": "string",
                    "description": (
                        "Full document content. "
                        "Prefix headings with '# '. "
                        "For xlsx, separate columns with '|'."
                    ),
                },
            },
            "required": ["format", "content"],
        },
    },
}

_MAX_ITERATIONS = 5


def reply(message, history, knowledge_base=""):
    """Agentic loop: call the model, execute tool calls, feed results back, repeat.

    message:        the latest text written by the user
    history:        list of previous messages
    knowledge_base: plain text extracted from uploaded documents (may be empty)

    Returns (final_text, list_of_tool_args).
    Each tool_arg is {"format": "docx"|"pdf"|"xlsx", "content": "..."}.
    The list is empty when no documents were requested.
    """
    system = SYSTEM_PROMPT
    if knowledge_base:
        system += (
            "\n\nThe user has uploaded the following documents as a knowledge base. "
            "Use them to answer questions when relevant.\n\n" + knowledge_base
        )

    # Bedrock requires conversations to start with a user message, so the system
    # prompt is injected as a hidden user/assistant exchange before the history.
    messages = [
        {"role": "user", "content": system},
        {"role": "assistant", "content": "Understood. How can I help you?"},
        *history,
        {"role": "user", "content": message},
    ]

    all_tool_args = []

    try:
        for iteration in range(1, _MAX_ITERATIONS + 1):
            yield ("step", f"Iteration {iteration}: calling the model…")

            # tool_choice is intentionally omitted: some adapters reject the parameter
            # even when its value is "auto", while still honouring the tools list.
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=[_DOCUMENT_TOOL],
                max_tokens=MAX_TOKENS,
            )
            choice = response.choices[0]
            finish = choice.finish_reason or "unknown"

            if choice.message.tool_calls:
                tool_call = choice.message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                tool_args = {
                    "format": args.get("format", "docx"),
                    "content": args.get("content", ""),
                }
                all_tool_args.append(tool_args)
                yield ("tool", tool_args)

                # Feed the tool result back so the model can continue reasoning.
                messages.append({
                    "role": "assistant",
                    "content": choice.message.content or "",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                    ],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": (
                        f"Document created successfully in "
                        f"{tool_args['format'].upper()} format."
                    ),
                })
                yield ("step", f"Iteration {iteration}: tool called → create_document({tool_args['format']}). Feeding result back…")

            elif finish == "length":
                # Response was cut by the token limit — warn and surface what arrived.
                yield ("step", (
                    f"⚠️ Iteration {iteration}: response cut off (finish_reason='length'). "
                    f"Try increasing MAX_TOKENS in config.py (currently {MAX_TOKENS})."
                ))
                yield ("done", choice.message.content or "")
                return

            else:
                yield ("step", f"Iteration {iteration}: finish_reason={finish!r} — no tool call, loop complete.")
                yield ("done", choice.message.content or "")
                return

        # Safety: max iterations reached.
        yield ("step", f"Reached max iterations ({_MAX_ITERATIONS}), stopping.")
        yield ("done", "")

    except (PermissionDeniedError, BadRequestError) as exc:
        yield ("step", f"⚠️ Tool call failed: {exc}")
        yield ("step", "Falling back to plain text (tools not supported by this model)…")
        # The current model does not support tool calling — fall back to plain chat.
        response = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=MAX_TOKENS)
        text = (response.choices[0].message.content or "") + (
            "\n\n---\n"
            "⚠️ **Document generation is not available:** "
            "the current model does not support tool calls. "
            "Switch to a model that supports function calling to use this feature."
        )
        yield ("done", text)
