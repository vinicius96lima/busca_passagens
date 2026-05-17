from datetime import datetime
from src.emails.voo_VIX import enviar_email_vix
from src.emails.voo_POA import enviar_email_poa
from src.search.buscar_passagens import buscar_passagens
from src.extract.insert_sql import inserir_base
from src.extract.salvar_voos import salvar_voo
from src.extract.integracao_whats import send_message
from src.metodos_azure_outlook.move_emails_voos import move_emails_voos
from src.metodos_azure_outlook.move_emals_failed import move_emails_failed
import traceback


def main():
    print(f"\n🔍 Iniciando busca: {datetime.today().strftime('%d/%m/%Y %H:%M')}")
    voos = buscar_passagens(
        origens=["GRU", "CGH", "VCP"],
        destinos=["POA", "VIX"],
        data_ida="2026-09-04",
        data_volta="2026-09-07",
        valor_maximo=1500.00,
        adultos=2
    )

    salvar_voos = salvar_voo(voos)
    inserir_base(salvar_voos)
    voo_poa = enviar_email_poa(voos)
    voo_vix = enviar_email_vix(voos)
    send_message(voo_poa, voo_vix)
    print(f"✅ Busca finalizada: {datetime.today().strftime('%d/%m/%Y %H:%M')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERRO:")
        print(e)
        traceback.print_exc()
        main()




