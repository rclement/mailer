import requests


verify_url = "https://www.google.com/recaptcha/api/siteverify"


def verify(secret_key: str | None, response: str | None) -> None:
    if secret_key:
        params = {"secret": secret_key, "response": response}
        rv = requests.post(verify_url, data=params, timeout=30)
        rv_json = rv.json()

        if rv.status_code != 200 or not rv_json.get("success", False):
            raise RuntimeError
