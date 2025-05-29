import json
def parse_json(response_content: str) -> dict:
    try:
        output = json.loads(response_content)
    except:
        raise TypeError(f"Raw output: {response_content}")
    return output
