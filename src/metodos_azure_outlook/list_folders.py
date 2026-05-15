from src.services.conexao_outlook import connect_azure
import requests


def listar_pastas(connect):
    connect = connect_azure()
    logs_git = 'AQMkADAwATZiZmYAZC1kZTJkLTkwZDgtMDACLTAwCgAuAAADDdyhqGorrEiSyhiPP3efawEASRx-dnXjtU6Ab0sZ3kK92wAGjJJg9gAAAA=='
    caixa_entrada = 'AQMkADAwATZiZmYAZC1kZTJkLTkwZDgtMDACLTAwCgAuAAADDdyhqGorrEiSyhiPP3efawEASRx-dnXjtU6Ab0sZ3kK92wAAAgEMAAAA'
    url = f"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/childFolders"
    res = requests.get(url, headers=headers)
    pastas = res.json()
    for pasta in pastas["value"]:
        print(
            pasta["displayName"],
            "->",
            pasta["id"]
        )

