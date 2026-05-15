import os
import msal
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TOKEN_CACHE = os.getenv("TOKENAZUREGIT")

CACHE_FILE = "token_cache.bin"


def connect_azure():

    # recria token_cache.bin a partir do secret
    if TOKEN_CACHE and not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "wb") as f:
            f.write(base64.b64decode(TOKEN_CACHE))

    cache = msal.SerializableTokenCache()

    # carrega cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/consumers",
        token_cache=cache
    )

    scopes = [
        "Mail.Send",
        "Mail.ReadWrite",
        "User.Read"
    ]

    accounts = app.get_accounts()

    if not accounts:
        raise Exception(
            "Nenhuma conta encontrada no cache. Gere o token localmente novamente."
        )

    # tenta renovar silenciosamente
    result = app.acquire_token_silent(
        scopes=scopes,
        account=accounts[0]
    )

    if not result or "access_token" not in result:
        raise Exception(
            "Token expirado ou inválido. Gere novo token localmente."
        )

    # salva cache atualizado
    with open(CACHE_FILE, "w") as f:
        f.write(cache.serialize())

    access_token = result["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    return headers