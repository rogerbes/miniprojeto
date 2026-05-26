from funcoes import processar_produtos, processar_pedidos

def main():
    # Definição dos caminhos dos arquivos (certifique-se de baixar os arquivos do repositório indicado)
    # URL da Base de dados: https://github.com/fiesc-junior-prado/mine_projeto_bloco_1
    
    arquivo_produtos_in = "olist_products_dataset.csv"
    arquivo_produtos_out = "olist_products_sanitized.csv"
    
    arquivo_pedidos_in = "olist_orders_dataset.csv"
    arquivo_pedidos_out = "olist_orders_sanitized.csv"
    
    print("="*60)
    print(" INICIANDO PIPELINE DE SANITIZAÇÃO DE DADOS (OLIST) ")
    print("="*60)
    
    # 1. Processamento de Produtos
    print("\n[1/2] Processando arquivo de produtos...")
    res_produtos = processar_produtos(arquivo_produtos_in, arquivo_produtos_out)
    
    # 2. Processamento de Pedidos
    print("[2/2] Processando arquivo de pedidos...")
    res_pedidos = processar_pedidos(arquivo_pedidos_in, arquivo_pedidos_out)
    
    # 3. Exibição do Relatório de Status Manual (Tarefa 5)
    print("\n" + "="*60)
    print(" RELATÓRIO ESTATÍSTICO DE SANITIZAÇÃO ")
    print("="*60)
    print(f"Total de produtos lidos: {res_produtos['processados']}")
    print(f"Total de categorias vazias corrigidas: {res_produtos['nulos_categoria_corrigidos']}")
    print(f"Total de produtos descartados (dimensões ausentes): {res_produtos['linhas_descartadas']}")
    print("-"*40)
    print(f"Total de pedidos lidos: {res_pedidos['processados']}")
    print(f"Total de pedidos cancelados identificados: {res_pedidos['cancelados_identificados']}")
    print(f"Total de pedidos com data de entrega ausente: {res_pedidos['total_vazios_entrega']}")
    
    # Validação analítica da hipótese levantada pela diretoria
    print("-"*40)
    print("VALIDAÇÃO DA HIPÓTESE DA DIRETORIA:")
    vazios_totais = res_pedidos['total_vazios_entrega']
    vazios_por_cancelamento = res_pedidos['hipotese_verdadeira']
    
    if vazios_totais == 0:
        print(" > Não foram encontrados registros com data de entrega vazia.")
    elif vazios_totais == vazios_por_cancelamento:
        print(" > Hipótese COMPROVADA: Todas as datas de entrega nulas devem-se estritamente a pedidos cancelados.")
    else:
        diferenca = vazios_totais - vazios_por_cancelamento
        print(f" > Hipótese REJEITADA: Das {vazios_totais} entregas vazias, apenas {vazios_por_cancelamento} ")
        print(f"   foram canceladas. Existem {diferenca} pedidos com outras justificativas (ex: em trânsito/indisponíveis).")
    
    print("="*60)
    print("Pipeline concluído com sucesso! Arquivos sanitizados gerados.")

if __name__ == "__main__":
    main()