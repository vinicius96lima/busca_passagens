from datetime import datetime
from voo_VIX import enviar_email_vix
from voo_POA import enviar_email_poa
from buscar_passagens import buscar_passagens
from insert_sql import inserir_base
from salvar_voos import salvar_voo
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
    insert_sql = inserir_base(salvar_voos)
    voo_poa = enviar_email_poa(voos)
    voo_vix = enviar_email_vix(voos)
    print(f"✅ Busca finalizada: {datetime.today().strftime('%d/%m/%Y %H:%M')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERRO:")
        print(e)
        traceback.print_exc()
        raise
        main()




