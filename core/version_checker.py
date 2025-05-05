import requests
from config.global_state import TOOLKIT_VERSION

def fetch_update_info(url: str):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return {"raw_text": response.text}
        return {}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def compare_versions(now: str, latest: str) -> int:
    now_parts = list(map(int, now.strip("Vv").split(".")))
    latest_parts = list(map(int, latest.strip("Vv").split(".")))
    return (now_parts > latest_parts) - (now_parts < latest_parts)
