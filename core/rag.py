import requests
import streamlit as st
import json

def call_mistral_api(system_msg, messages):
    api_key = st.secrets.get("MISTRAL_API_KEY")

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "system", "content": system_msg}] + messages,
        "stream": True
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:
            st.error(f"Erro da API: {response.text}")
            return None

        return response

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None


def stream_response(response):
    full_resp = ""

    for line in response.iter_lines():
        if line:
            try:
                line_text = line.decode("utf-8").strip()

                if line_text.startswith("data: "):
                    data = line_text[6:].strip()

                    if data == "[DONE]":
                        break

                    data_json = json.loads(data)

                    delta = data_json["choices"][0].get("delta", {})
                    content = delta.get("content", "")

                    full_resp += content
                    yield full_resp

            except:
                continue

    return full_resp
