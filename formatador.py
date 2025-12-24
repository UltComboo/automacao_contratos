# formatador.py - VERSÃO COMPLETA
"""
Módulo para formatação de dados conforme especificações
"""

import re
from datetime import datetime
from config import MESES_PT, SIGLAS_ESTADOS, ABREVIACOES


class FormatadorDados:
    @staticmethod
    def formatar_nome_completo(nome):
        """
        Formata nome completo para MAIÚSCULAS
        """
        if not nome or not isinstance(nome, str):
            return ""

        # Remover espaços extras e colocar em maiúsculas
        nome_formatado = ' '.join(nome.split()).upper()

        return nome_formatado

    @staticmethod
    def formatar_cpf(cpf):
        """
        Formata CPF: aceita qualquer entrada, sai com pontos e traço
        Ex: 00000000000 -> 000.000.000-00
        """
        if not cpf:
            return ""

        # Remover todos os caracteres não numéricos
        cpf_limpo = re.sub(r'[^\d]', '', str(cpf))

        # Verificar se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return cpf_limpo  # Retorna como está se não for válido

        # Formatar: 000.000.000-00
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

    @staticmethod
    def formatar_endereco(endereco):
        """
        Formata endereço: Primeira letra maiúscula e aplica abreviações
        """
        if not endereco or not isinstance(endereco, str):
            return ""

        # Remover espaços extras
        endereco = ' '.join(endereco.split())

        # Converter para minúsculas para processamento
        endereco_lower = endereco.lower()

        # Aplicar abreviações
        palavras = endereco_lower.split()
        palavras_formatadas = []

        for palavra in palavras:
            # Verificar se a palavra tem abreviação
            if palavra in ABREVIACOES:
                palavras_formatadas.append(ABREVIACOES[palavra])
            else:
                # Capitalizar primeira letra de cada palavra
                if palavra:
                    palavras_formatadas.append(palavra.capitalize())
                else:
                    palavras_formatadas.append(palavra)

        # Juntar novamente
        endereco_formatado = ' '.join(palavras_formatadas)

        # Garantir que números venham após vírgula
        endereco_formatado = re.sub(r'(\d+)\s*,', r'\1,', endereco_formatado)

        return endereco_formatado

    @staticmethod
    def formatar_cidade(cidade):
        """
        Formata cidade: Primeira letra maiúscula
        Ex: SÃO PAULO -> São Paulo
        """
        if not cidade or not isinstance(cidade, str):
            return ""

        # Remover espaços extras
        cidade = ' '.join(cidade.split())

        # Converter para título, mas manter certas palavras em maiúsculo
        palavras_especiais = ['de', 'da', 'do', 'das', 'dos', 'e']

        palavras = cidade.split()
        palavras_formatadas = []

        for i, palavra in enumerate(palavras):
            palavra_lower = palavra.lower()

            if palavra_lower in palavras_especiais and i > 0:
                palavras_formatadas.append(palavra_lower)
            else:
                # Capitalizar primeira letra
                palavras_formatadas.append(palavra.capitalize())

        return ' '.join(palavras_formatadas)

    @staticmethod
    def formatar_estado(sigla):
        """
        Formata estado: sigla em MAIÚSCULAS
        """
        if not sigla or not isinstance(sigla, str):
            return ""

        sigla = sigla.strip().upper()

        # Verificar se é uma sigla válida
        if sigla in SIGLAS_ESTADOS:
            return sigla
        else:
            return sigla  # Retorna como está, mas em maiúsculas

    @staticmethod
    def formatar_oab(numero_oab):
        """
        Formata número da OAB: XXX.XXX
        """
        if not numero_oab:
            return ""

        # Remover caracteres não numéricos
        numero_limpo = re.sub(r'[^\d]', '', str(numero_oab))

        # Formatar: XXX.XXX
        if len(numero_limpo) == 6:
            return f"{numero_limpo[:3]}.{numero_limpo[3:]}"
        else:
            return numero_limpo  # Retorna como está se não for 6 dígitos

    @staticmethod
    def formatar_estado_civil(estado_civil, genero='masculino'):
        """
        Formata estado civil conforme gênero (minúsculas)
        """
        if not estado_civil:
            return ""

        estado_civil = estado_civil.strip().lower()

        # Mapeamento de estados civis por gênero
        estados = {
            'masculino': {
                'solteiro': 'solteiro',
                'casado': 'casado',
                'divorciado': 'divorciado',
                'viúvo': 'viúvo',
                'viuvo': 'viúvo',
                'separado': 'separado'
            },
            'feminino': {
                'solteiro': 'solteira',
                'casado': 'casada',
                'divorciado': 'divorciada',
                'viúvo': 'viúva',
                'viuvo': 'viúva',
                'separado': 'separada'
            }
        }

        # Tentar encontrar correspondência
        for entrada, saida in estados[genero].items():
            if entrada in estado_civil:
                return saida

        # Se não encontrar, retornar como está em minúsculas
        return estado_civil

    @staticmethod
    def formatar_data(data_str):
        """
        Formata data: entrada 23/12/2025 -> saída 23 de dezembro de 2025
        RETORNA APENAS A DATA, SEM A CIDADE
        """
        if not data_str:
            # Usar data atual como padrão
            data = datetime.now()
        else:
            try:
                # Tentar vários formatos de data
                formatos = ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%Y-%m-%d']
                data = None

                for formato in formatos:
                    try:
                        data = datetime.strptime(data_str.strip(), formato)
                        break
                    except ValueError:
                        continue

                if not data:
                    raise ValueError("Formato de data não reconhecido")

            except Exception:
                # Se não conseguir parsear, usar data atual
                data = datetime.now()

        # Formatar: 23 de dezembro de 2025 (APENAS A DATA)
        return f"{data.day} de {MESES_PT[data.month]} de {data.year}"

    @staticmethod
    def determinar_genero(nome_completo):
        """
        Tenta determinar o gênero pelo nome para formatar estado civil
        """
        if not nome_completo:
            return 'masculino'

        # Nomes tipicamente femininos (sufixos comuns)
        sufixos_femininos = ['a', 'e', 'ia', 'na', 'ra', 'la']

        # Pegar o primeiro nome
        primeiro_nome = nome_completo.split()[0].lower() if nome_completo.split() else ""

        # Verificar sufixos
        for sufixo in sufixos_femininos:
            if primeiro_nome.endswith(sufixo):
                return 'feminino'

        return 'masculino'