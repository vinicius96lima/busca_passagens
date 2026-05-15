import os
import msal
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")

def connect_azure():
    cache = msal.SerializableTokenCache()
    if os.path.exists("../token_cache.bin"):
        with open("../token_cache.bin", "r") as f:
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
    result = None
    if accounts:
        result = app.acquire_token_silent(
            scopes=scopes,
            account=accounts[0]
        )
    if not result:
        result = app.acquire_token_interactive(scopes=scopes)
    with open("../token_cache.bin", "w") as f:
        f.write(cache.serialize())
    with open("../token_cache.bin", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    access_token = result["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers

