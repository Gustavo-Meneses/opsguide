import re

def extract_code(text):
    match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.S)
    if match:
        return match.group(1)
    return None


def extract_mermaid(text):
    if "```mermaid" in text:
        try:
            return text.split("```mermaid")[-1].split("```")[0]
        except:
            return None
    return None
