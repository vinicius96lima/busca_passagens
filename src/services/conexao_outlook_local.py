# get_token.py — roda localmente UMA VEZ para pegar o refresh_token
import msal
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')  # para conta pessoal — não use o tenant ID corporativo
print(f"Token lido ({len(TENANT_ID)} chars): {TENANT_ID[:30]}...")

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/common"  # testa com common
)

flow = app.initiate_device_flow(scopes=["Mail.Read", "Mail.ReadWrite"])
print(flow["message"])

result = app.acquire_token_by_device_flow(flow)

if "refresh_token" in result:
    print("\n✅ Novo refresh_token:\n")
    print(result["refresh_token"])
    print(f"\nTamanho: {len(result['refresh_token'])} chars")
else:
    print("Erro:", result)