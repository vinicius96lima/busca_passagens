import os
import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
REFRESH_TOKEN = os.getenv("TOKENAZUREGIT")
SCOPES = ["Mail.Read", "Mail.ReadWrite"]

def connect_azure():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/common"
    )

    # Usa o refresh_token para obter novo access_token sem login
    result = app.acquire_token_by_refresh_token(REFRESH_TOKEN, scopes=SCOPES)
    #print("RESULTADO COMPLETO:", result)

    if "access_token" not in result:
        raise Exception(f"Falha ao renovar token: {result.get('error_description')}")

    return {"Authorization": f"Bearer {result['access_token']}", "Content-Type": "application/json"}
