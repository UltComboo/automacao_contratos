# main.py
"""
Sistema de Geração de Contratos - Silveiro Advogados
Com inputs formatados conforme especificações
"""

import os
import re
from datetime import datetime
from gerador import gerar_todos_contratos
from formatador import FormatadorDados
from config import SIGLAS_ESTADOS

# Defina ESTADOS_CIVIS localmente no main.py
ESTADOS_CIVIS = {
    '1': 'solteiro',
    '2': 'casado',
    '3': 'divorciado',
    '4': 'viúvo',
    '5': 'separado'
}


class ColetorDados:
    def __init__(self):
        self.formatador = FormatadorDados()
        self.dados = {}

    def coletar_nome_completo(self):
        """Coleta e formata nome completo"""
        print("\n👤 DADOS PESSOAIS")
        print("-" * 40)

        while True:
            nome = input("Nome completo: ").strip()
            if nome:
                # Formatar para MAIÚSCULAS
                self.dados['nome_completo'] = self.formatador.formatar_nome_completo(nome)
                break
            else:
                print("❌ Nome é obrigatório. Tente novamente.")

    def coletar_cpf(self):
        """Coleta e formata CPF"""
        while True:
            cpf = input("CPF (qualquer formato): ").strip()
            if cpf:
                # Formatar CPF com pontos e traço
                cpf_formatado = self.formatador.formatar_cpf(cpf)

                # Verificar se a formatação resultou em um CPF válido
                if len(re.sub(r'[^\d]', '', cpf_formatado)) == 11:
                    self.dados['cpf'] = cpf_formatado
                    print(f"   ✓ CPF formatado: {cpf_formatado}")
                    break
                else:
                    print("❌ CPF inválido. Digite 11 números.")
            else:
                print("❌ CPF é obrigatório.")

    def coletar_endereco(self):
        """Coleta e formata endereço"""
        print("\n📍 ENDEREÇO")
        print("-" * 40)

        while True:
            endereco = input("Endereço completo (ex: Av. Paulista, 123, apto 101): ").strip()
            if endereco:
                # Formatar: primeira letra maiúscula e abreviações
                endereco_formatado = self.formatador.formatar_endereco(endereco)
                self.dados['endereco_completo'] = endereco_formatado
                print(f"   ✓ Endereço formatado: {endereco_formatado}")
                break
            else:
                print("❌ Endereço é obrigatório.")

    def coletar_cidade_estado(self):
        """Coleta e formata cidade e estado"""
        # Cidade
        while True:
            cidade = input("Cidade: ").strip()
            if cidade:
                # Formatar: Primeira letra maiúscula
                cidade_formatada = self.formatador.formatar_cidade(cidade)
                self.dados['cidade'] = cidade_formatada
                print(f"   ✓ Cidade formatada: {cidade_formatada}")
                break
            else:
                print("❌ Cidade é obrigatória.")

        # Estado (sigla)
        while True:
            estado = input("Estado (sigla, ex: SP): ").strip().upper()
            if estado in SIGLAS_ESTADOS:
                # Formatar: MAIÚSCULAS
                estado_formatado = self.formatador.formatar_estado(estado)
                self.dados['estado'] = estado_formatado
                print(f"   ✓ Estado: {estado_formatado}")
                break
            else:
                print(f"❌ Sigla de estado inválida. Use: {', '.join(sorted(SIGLAS_ESTADOS.keys()))}")

    def coletar_dados_profissionais(self):
        """Coleta dados profissionais"""
        print("\n⚖️ DADOS PROFISSIONAIS")
        print("-" * 40)

        # OAB
        while True:
            oab = input("Número da OAB (6 dígitos): ").strip()
            if oab:
                # Formatar: XXX.XXX
                oab_formatado = self.formatador.formatar_oab(oab)
                if len(re.sub(r'[^\d]', '', oab_formatado)) == 6:
                    self.dados['oab_numero'] = oab_formatado
                    print(f"   ✓ OAB formatada: {oab_formatado}")
                    break
                else:
                    print("❌ Número da OAB deve ter 6 dígitos.")
            else:
                print("❌ Número da OAB é obrigatório.")

        # UF da OAB
        while True:
            uf_oab = input("UF da OAB (sigla): ").strip().upper()
            if uf_oab in SIGLAS_ESTADOS:
                self.dados['oab_uf'] = uf_oab
                break
            else:
                print(f"❌ Sigla de estado inválida.")

    def coletar_estado_civil(self):
        """Coleta e formata estado civil"""
        print("\n💍 ESTADO CIVIL")
        print("-" * 40)
        print("Opções:")
        print("1 - Solteiro(a)")
        print("2 - Casado(a)")
        print("3 - Divorciado(a)")
        print("4 - Viúvo(a)")
        print("5 - Separado(a)")

        while True:
            opcao = input("Escolha uma opção (1-5): ").strip()
            if opcao in ESTADOS_CIVIS:
                estado_civil = ESTADOS_CIVIS[opcao]

                # Determinar gênero pelo nome para formatar corretamente
                genero = self.formatador.determinar_genero(self.dados.get('nome_completo', ''))

                # Formatar conforme gênero (minúsculas)
                estado_civil_formatado = self.formatador.formatar_estado_civil(estado_civil, genero)
                self.dados['estado_civil'] = estado_civil_formatado
                print(f"   ✓ Estado civil: {estado_civil_formatado}")
                break
            else:
                print("❌ Opção inválida. Escolha de 1 a 5.")

    def coletar_data(self):
        """Coleta e formata data"""
        print("\n📅 DATA")
        print("-" * 40)
        print("Formato aceito: DD/MM/AAAA (ex: 23/12/2025)")
        print("Ou pressione Enter para usar a data atual")

        data_input = input("Data (DD/MM/AAAA): ").strip()

        # Formatar data: 23 de dezembro de 2025
        data_formatada = self.formatador.formatar_data(data_input)
        self.dados['data_formatada'] = data_formatada

        print(f"   ✓ Data formatada: {data_formatada}")

    def coletar_todos_dados(self):
        """Coleta todos os dados"""
        print("=" * 60)
        print("SISTEMA DE GERAÇÃO DE CONTRATOS - SILVEIRO ADVOGADOS")
        print("=" * 60)

        # Coletar dados em sequência
        self.coletar_nome_completo()
        self.coletar_cpf()
        self.coletar_endereco()
        self.coletar_cidade_estado()
        self.coletar_dados_profissionais()
        self.coletar_estado_civil()
        self.coletar_data()

        # Dados fixos
        self.dados.update({
            'profissao': 'advogado',
            'nacionalidade': 'brasileiro',
        })

        return self.dados

    def mostrar_resumo(self):
        """Mostra resumo dos dados coletados"""
        print("\n" + "=" * 60)
        print("RESUMO DOS DADOS")
        print("=" * 60)

        campos = [
            ("Nome completo", 'nome_completo'),
            ("CPF", 'cpf'),
            ("Endereço", 'endereco_completo'),
            ("Cidade/Estado", lambda d: f"{d.get('cidade', '')}/{d.get('estado', '')}"),
            ("OAB", lambda d: f"{d.get('oab_uf', '')} {d.get('oab_numero', '')}"),
            ("Estado civil", 'estado_civil'),
            ("Data", 'data_formatada'),
        ]

        for label, campo in campos:
            if callable(campo):
                valor = campo(self.dados)
            else:
                valor = self.dados.get(campo, '')

            print(f"{label:20}: {valor}")

        print("=" * 60)


def main():
    """Função principal"""
    try:
        # Coletor de dados
        coletor = ColetorDados()
        dados = coletor.coletar_todos_dados()

        # Mostrar resumo
        coletor.mostrar_resumo()

        # Confirmar
        resposta = input("\n✅ Confirmar e gerar contratos? (S/N): ").strip().upper()
        if resposta != 'S':
            print("\n❌ Operação cancelada.")
            return

        # Verificar templates
        templates = [
            "templates/PROCURACAO_MODEL.docx",
            "templates/TERMO DE AUTORIZAÇÃO DE IMAGEM_MODEL.docx",
            "templates/TERMO DE CONFIDENCIALIDADE_MODEL.docx",
            "templates/TERMO DE PROTEÇÃO DE DADOS_MODEL.docx"
        ]

        faltantes = []
        for template in templates:
            if not os.path.exists(template):
                faltantes.append(os.path.basename(template))

        if faltantes:
            print("\n⚠️  Templates não encontrados:")
            for template in faltantes:
                print(f"   - {template}")
            print("\nColoque os templates na pasta 'templates/'.")
            return

        # Gerar contratos
        print("\n" + "=" * 60)
        print("GERANDO CONTRATOS...")
        print("=" * 60)

        from gerador import gerar_todos_contratos
        resultados = gerar_todos_contratos(dados)

        # Resultados
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)

        sucessos = 0
        for nome, caminho in resultados:
            if caminho and os.path.exists(caminho):
                print(f"✅ {nome:25} - {os.path.basename(caminho)}")
                sucessos += 1
            else:
                print(f"❌ {nome:25} - FALHA")

        print("\n" + "=" * 60)
        print(f"📊 {sucessos}/4 contratos gerados com sucesso")

        if sucessos > 0:
            print(f"📁 Pasta de saída: {os.path.abspath('output')}")

        print("\n✨ Processo concluído!")

    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n💥 ERRO: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Criar pastas necessárias
    os.makedirs("templates", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Executar
    main()