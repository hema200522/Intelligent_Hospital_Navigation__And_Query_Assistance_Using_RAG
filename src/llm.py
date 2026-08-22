import os
import requests
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def generate_answer(question, context):

    prompt = f"""
You are CareCompass, an intelligent hospital information assistant.

Answer the user's question using ONLY the hospital information
provided in the context below.

Do not invent doctors, treatments, departments, room numbers,
hospital timings, policies, or medical information.

If the answer is not available in the context, say:

"I could not find this information in the hospital database."

For medical treatment questions, provide only the information
available in the hospital database and do not diagnose the patient.

HOSPITAL CONTEXT:
{context}

USER QUESTION:
{question}
"""

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    response = requests.post(
        NVIDIA_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]