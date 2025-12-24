# config.py - VERSÃO COMPLETA
"""
Configurações do sistema de geração de contratos
"""

# Dados fixos da sociedade
SOCIEDADE = {
    "nome": "SILVEIRO ADVOGADOS",
    "cnpj": "00.727.418/0001-03",
    "sede": "Av. Carlos Gomes, 258 - 9º andar, Porto Alegre/RS",
    "sede_cidade": "Porto Alegre",
}

# Outorgados fixos
OUTORGADOS = {
    "outorgado_1": {
        "nome": "RAFAEL BRAUDE CANTERJI",
        "cpf": "806.718.290-68",
        "oab_rs": "56.110",
        "oab_sp": "456.241"
    },
    "outorgado_2": {
        "nome": "RICARDO LEAL DE MORAES",
        "cpf": "962.155.770-49",
        "oab_rs": "56.486",
        "oab_sp": "325.160"
    }
}

# Mapeamento de meses em português
MESES_PT = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}

# Mapeamento de estados
SIGLAS_ESTADOS = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
    'MG': 'Mato Grosso', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
    'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
    'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
}

# Opções de estado civil para menu
ESTADOS_CIVIS = {
    '1': 'solteiro',
    '2': 'casado',
    '3': 'divorciado',
    '4': 'viúvo',
    '5': 'separado'
}

# Abreviações padrão para endereços
ABREVIACOES = {
    'avenida': 'Av.',
    'avendia': 'Av.',
    'av': 'Av.',
    'rua': 'R.',
    'travessa': 'Trav.',
    'trav': 'Trav.',
    'alameda': 'Al.',
    'al': 'Al.',
    'praça': 'Pça',
    'praca': 'Pça',
    'rodovia': 'Rod.',
    'rod': 'Rod.',
    'estrada': 'Est.',
    'est': 'Est.',
    'número': 'nº',
    'numero': 'nº',
    'n°': 'nº',
    'apartamento': 'apto',
    'apto': 'apto',
    'apartmento': 'apto',
    'bloco': 'bl.',
    'bl': 'bl.',
    'sala': 'sala',
    'andar': 'andar',
    'conjunto': 'cj.',
    'cj': 'cj.'
}

# Palavras/frases que DEVEM ficar em negrito (não são placeholders)
PALAVRAS_NEGRITO = [
    "OUTORGANTE:",
    "PROCURAÇÃO",
    "OUTORGADOS:",
    "RAFAEL BRAUDE CANTERJI",
    "RICARDO LEAL DE MORAES",
    "SOCIEDADE:",
    "SILVEIRO ADVOGADOS",
    "VALIDADE:",
    "TERMO DE AUTORIZAÇÃO E LIBERAÇÃO DE USO DE IMAGEM E VOZ",
    "TERMO DE CONFIDENCIALIDADE",
    "FINS E PODERES:",
    "TERMO DE PROTEÇÃO DE DADOS",
]