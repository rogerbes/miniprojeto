import csv
import re
import os
from datetime import datetime

def limpar_categoria(nome_categoria):
    """
    Tarefa 2: Padroniza strings e aplica Regex para limpar caracteres especiais.
    Garante letras minúsculas e remove espaços.
    """
    if not nome_categoria:
        return "sem categoria"
    
    # Converte para minúsculas e remove espaços no início/fim
    nome_limpo = nome_categoria.lower().strip()
    
    # Mantém apenas letras, números e espaços simples (remove pontuações indevidas)
    nome_limpo = re.sub(r'[^a-z0-9_\s-]', '', nome_limpo)
    
    return nome_limpo


def formatar_data(data_str):
    """
    Tarefa 4: Converte a data do formato original "YYYY-MM-DD HH:MM:SS"
    para o formato brasileiro "DD/MM/YYYY".
    """
    if not data_str or data_str.strip() == "":
        return ""
    try:
        # Faz o parse da string original
        objeto_data = datetime.strptime(data_str.strip(), "%Y-%m-%d %H:%M:%S")
        # Retorna no formato brasileiro simplificado
        return objeto_data.strftime("%d/%m/%Y") # Nota: %Y para ano com 4 dígitos
    except ValueError:
        # Caso a string esteja fora do padrão esperado
        return data_str


def processar_produtos(caminho_input, caminho_output):
    """
    Tarefa 1 e 2: Lê o arquivo de produtos, trata nulos/vazios e limpa strings.
    
    Decisão Técnica sobre Dimensões Físicas (Product dimensions):
    Optou-se por DESCARTAR as linhas que possuem dimensões físicas nulas (Ex: peso, comprimento).
    Justificativa: Para modelos logísticos ou de precificação de frete (comuns na Olist), 
    atribuir uma média arbitrária pode enviesar o cálculo do frete real, sendo mais seguro 
    remover a inconsistência da amostragem principal.
    """
    totais = {"processados": 0, "nulos_categoria_corrigidos": 0, "linhas_descartadas": 0}
    
    if not os.path.exists(caminho_input):
        print(f"Erro: Arquivo {caminho_input} não encontrado.")
        return totais

    with open(caminho_input, mode='r', encoding='utf-8') as f_in, \
         open(caminho_output, mode='w', encoding='utf-8', newline='') as f_out:
        
        leitor = csv.DictReader(f_in)
        campos = leitor.fieldnames
        
        escritor = csv.DictWriter(f_out, fieldnames=campos)
        escritor.writeheader()
        
        for linha in leitor:
            totais["processados"] += 1
            
            # Verificação de dimensões físicas nulas
            dimensoes = [
                linha.get('product_weight_g'),
                linha.get('product_length_cm'),
                linha.get('product_height_cm'),
                linha.get('product_width_cm')
            ]
            
            if any(v is None or v.strip() == "" for v in dimensoes):
                totais["linhas_descartadas"] += 1
                continue # Descarta o registro pulando para a próxima iteração
            
            # Tratamento da categoria vazia
            cat = linha.get('product_category_name', '')
            if not cat or cat.strip() == "":
                linha['product_category_name'] = "Sem Categoria"
                totais["nulos_categoria_corrigidos"] += 1
            else:
                linha['product_category_name'] = limpar_categoria(cat)
                
            escritor.writerow(linha)
            
    return totais


def processar_pedidos(caminho_input, caminho_output):
    """
    Tarefa 3 e 4: Trata o arquivo de pedidos, valida a hipótese de cancelamento
    e formata os campos temporais.
    """
    totais = {"processados": 0, "cancelados_identificados": 0, "hipotese_verdadeira": 0, "total_vazios_entrega": 0}
    
    if not os.path.exists(caminho_input):
        print(f"Erro: Arquivo {caminho_input} não encontrado.")
        return totais

    with open(caminho_input, mode='r', encoding='utf-8') as f_in, \
         open(caminho_output, mode='w', encoding='utf-8', newline='') as f_out:
        
        leitor = csv.DictReader(f_in)
        campos = leitor.fieldnames
        
        escritor = csv.DictWriter(f_out, fieldnames=campos)
        escritor.writeheader()
        
        for linha in leitor:
            totais["processados"] += 1
            
            status = linha.get('order_status', '').strip()
            data_entrega = linha.get('order_delivered_customer_date', '').strip()
            
            # Contagem de pedidos cancelados globalmente
            if status == 'canceled':
                totais["cancelados_identificados"] += 1
            
            # Análise da hipótese de negócio (Data de entrega vazia)
            if not data_entrega:
                totais["total_vazios_entrega"] += 1
                if status == 'canceled':
                    totais["hipotese_verdadeira"] += 1
            
            # Formatação Temporal da data de aprovação
            data_aprovacao = linha.get('order_approved_at', '')
            if data_aprovacao:
                linha['order_approved_at'] = formatar_data(data_aprovacao)
                
            escritor.writerow(linha)
            
    return totais