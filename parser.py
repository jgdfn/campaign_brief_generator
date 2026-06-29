"""
Wraps the call to GPT-5. In demo mode (no API key set), returns a
pre-built simulated response so the rest of the app can be tested
end to end before a real key exists.
"""

import json
import os

from prompts import SYSTEM_PROMPT, build_user_prompt

DEMO_RESPONSE_PATH = os.path.join(os.path.dirname(__file__), "test_outputs", "yummiez_simulated_response.json")


def is_demo_mode() -> bool:
    """Demo mode is on whenever no API key is configured."""
    return not bool(os.environ.get("OPENAI_API_KEY", "").strip())


def generate_brief(mom_text: str, extra_context: str = "") -> dict:
    """
    Returns a dict matching schema.py's RESPONSE_SHAPE_EXAMPLE.
    Falls back to the demo response if no API key is set, so the
    dashboard can be tested without live API costs.
    """
    if is_demo_mode():
        with open(DEMO_RESPONSE_PATH) as f:
            return json.load(f)

    return _call_openai(mom_text, extra_context)


def _call_openai(mom_text: str, extra_context: str) -> dict:
    from openai import OpenAI

    client = OpenAI()
    user_prompt = build_user_prompt(mom_text, extra_context)

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    raw_text = response.choices[0].message.content
    return json.loads(raw_text)
