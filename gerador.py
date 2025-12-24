# gerador.py - VERSÃO CORRIGIDA PARA NEGRITO
from docx import Document
from docx.shared import Pt
import os
import re
from datetime import datetime
from config import SOCIEDADE, OUTORGADOS, MESES_PT, PALAVRAS_NEGRITO


class GeradorContratos:
    def __init__(self):
        pass  # Removemos a dependência do FormatadorDados por enquanto

    def limpar_markdown(self, texto):
        """Remove formatação markdown (**) do texto"""
        # Remover ** do início e fim
        texto = texto.replace('**', '')
        # Remover > do início de linhas (formatação de citação)
        texto = re.sub(r'^>\s*', '', texto, flags=re.MULTILINE)
        return texto.strip()

    def extrair_titulo_negrito(self, texto):
        """Extrai o título que deve ficar em negrito (se houver **)"""
        # Verificar se há ** no texto
        if '**' in texto:
            # Encontrar texto entre **
            padrao = r'\*\*(.*?)\*\*'
            matches = re.findall(padrao, texto)
            if matches:
                return matches[0]  # Retorna o texto que estava entre **
        return None

    def preparar_placeholders(self, dados_pessoa):
        """Prepara placeholders simples"""
        # CORREÇÃO DA DATA
        data_formatada = dados_pessoa.get('data_formatada', '')

        # Se a data já tem "Porto Alegre/RS", usar como está
        if "Porto Alegre" in data_formatada and "RS" in data_formatada:
            data_assinatura = data_formatada
        else:
            # Adicionar cidade/estado apenas se não estiver presente
            data_assinatura = f"Porto Alegre/RS, {data_formatada}"

        return {
            "{{NOME_COMPLETO}}": dados_pessoa.get('nome_completo', ''),
            "{{CPF}}": dados_pessoa.get('cpf', ''),
            "{{CPF_OUTORGANTE}}": dados_pessoa.get('cpf', ''),
            "{{ENDERECO_COMPLETO}}": dados_pessoa.get('endereco_completo', ''),
            "{{CIDADE_ESTADO}}": f"{dados_pessoa.get('cidade', '')}/{dados_pessoa.get('estado', '')}",
            "{{ENDERECO_CIDADE}}": dados_pessoa.get('cidade', ''),
            "{{ENDERECO_ESTADO}}": dados_pessoa.get('estado', ''),
            "{{OAB_NUMERO}}": dados_pessoa.get('oab_numero', ''),
            "{{OAB_UF}}": dados_pessoa.get('oab_uf', ''),
            "{{ESTADO_CIVIL}}": dados_pessoa.get('estado_civil', ''),
            "{{BRASILEIRO_A}}": "brasileiro",
            "{{RESIDENTE_A}}": "residente e domiciliado",
            "{{ADVOGADO_A}}": "advogado",
            "{{SOCIEDADE_NOME}}": SOCIEDADE['nome'],
            "{{SOCIEDADE_CNPJ}}": SOCIEDADE['cnpj'],
            "{{DATA_ASSINATURA}}": data_assinatura,
            "{{NOME_ASSINATURA}}": dados_pessoa.get('nome_completo', ''),
            "{{SEDE}}": SOCIEDADE['sede_cidade'],
        }

    def deve_ficar_negrito(self, texto, nome_completo, titulo_negrito=None):
        """Verifica se o texto deve ficar em negrito"""
        texto_limpo = self.limpar_markdown(texto)

        # 1. Verificar se é um título que estava entre **
        if titulo_negrito and titulo_negrito in texto_limpo:
            return True

        # 2. Verificar nome completo
        if nome_completo and nome_completo in texto_limpo:
            # Verificar se é exatamente o nome ou contém como palavra completa
            if texto_limpo == nome_completo or re.search(rf'\b{nome_completo}\b', texto_limpo):
                return True

        # 3. Verificar palavras da lista (comparar com texto limpo)
        for palavra in PALAVRAS_NEGRITO:
            # Limpar a palavra também
            palavra_limpa = self.limpar_markdown(palavra)
            if palavra_limpa and palavra_limpa in texto_limpo:
                # Verificar se é uma palavra completa
                if re.search(rf'\b{re.escape(palavra_limpa)}\b', texto_limpo):
                    return True

        return False

    def processar_paragrafo_complexo(self, paragraph, placeholders, nome_completo):
        """Processa parágrafos complexos com múltiplas partes"""
        texto_original = paragraph.text

        # Extrair título que deve ficar em negrito (se houver **)
        titulo_negrito = self.extrair_titulo_negrito(texto_original)

        # Limpar markdown
        texto_limpo = self.limpar_markdown(texto_original)

        # Substituir placeholders
        for placeholder, valor in placeholders.items():
            if placeholder in texto_limpo:
                texto_limpo = texto_limpo.replace(placeholder, valor)

        # Decidir formatação
        if self.deve_ficar_negrito(texto_original, nome_completo, titulo_negrito):
            # Se deve ficar em negrito, aplicar em todo o parágrafo
            paragraph.clear()
            run = paragraph.add_run(texto_limpo)
            run.font.name = 'Arial Narrow'
            run.font.size = Pt(11)
            run.bold = True
        else:
            # Se não deve ficar em negrito
            paragraph.clear()
            run = paragraph.add_run(texto_limpo)
            run.font.name = 'Arial Narrow'
            run.font.size = Pt(11)
            run.bold = False

        return texto_limpo

    def processar_paragrafo_simples(self, paragraph, placeholders, nome_completo):
        """Processa parágrafos simples (sem **)"""
        texto_original = paragraph.text

        # Substituir placeholders
        texto_processado = texto_original
        for placeholder, valor in placeholders.items():
            if placeholder in texto_processado:
                texto_processado = texto_processado.replace(placeholder, valor)

        # Verificar se deve ficar em negrito
        deve_negrito = self.deve_ficar_negrito(texto_processado, nome_completo)

        # Atualizar parágrafo
        if texto_processado != texto_original or deve_negrito != paragraph.runs[0].bold:
            paragraph.clear()
            run = paragraph.add_run(texto_processado)
            run.font.name = 'Arial Narrow'
            run.font.size = Pt(11)
            run.bold = deve_negrito

        return texto_processado

    def gerar_contrato(self, template_path, dados_pessoa):
        """Gera contrato com tratamento especial para markdown"""
        try:
            placeholders = self.preparar_placeholders(dados_pessoa)
            nome_completo = dados_pessoa.get('nome_completo', '')

            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Template não encontrado: {template_path}")

            print(f"📄 Processando: {os.path.basename(template_path)}")

            # Carregar documento
            doc = Document(template_path)

            # PRIMEIRO: Identificar se é um documento com markdown (**)
            tem_markdown = False
            for paragraph in doc.paragraphs[:3]:  # Verificar primeiros parágrafos
                if '**' in paragraph.text:
                    tem_markdown = True
                    break

            # SEGUNDO: Processar parágrafos conforme o tipo
            for paragraph in doc.paragraphs:
                if not paragraph.text.strip():
                    continue  # Pular parágrafos vazios

                if tem_markdown and ('**' in paragraph.text or paragraph.text.startswith('>')):
                    # Processar como parágrafo complexo (com markdown)
                    self.processar_paragrafo_complexo(paragraph, placeholders, nome_completo)
                else:
                    # Processar como parágrafo simples
                    self.processar_paragrafo_simples(paragraph, placeholders, nome_completo)

            # TERCEIRO: Processar tabelas
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            if paragraph.text.strip():
                                self.processar_paragrafo_simples(paragraph, placeholders, nome_completo)

            # Nome do arquivo
            nome_base = os.path.splitext(os.path.basename(template_path))[0]
            nome_simplificado = nome_base.replace(" ", "_").replace("_MODEL", "")
            nome_pessoa = nome_completo.replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            nome_arquivo = f"{nome_simplificado}_{nome_pessoa}_{timestamp}.docx"
            output_path = os.path.join("output", nome_arquivo)

            # Salvar
            os.makedirs("output", exist_ok=True)
            doc.save(output_path)

            print(f"  ✅ Salvo: {nome_arquivo}")
            return output_path

        except Exception as e:
            print(f"✗ Erro ao gerar contrato: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


def gerar_todos_contratos(dados_pessoa):
    """Função principal"""
    gerador = GeradorContratos()

    templates = [
        ("templates/PROCURACAO_MODEL.docx", "Procuração"),
        ("templates/TERMO DE AUTORIZAÇÃO DE IMAGEM_MODEL.docx", "Autorização de Imagem"),
        ("templates/TERMO DE CONFIDENCIALIDADE_MODEL.docx", "Confidencialidade"),
        ("templates/TERMO DE PROTEÇÃO DE DADOS_MODEL.docx", "Proteção de Dados"),
    ]

    resultados = []

    for template_path, nome_contrato in templates:
        try:
            caminho = gerador.gerar_contrato(template_path, dados_pessoa)
            resultados.append((nome_contrato, caminho))
        except Exception as e:
            print(f"  ✗ Falha no {nome_contrato}: {str(e)}")
            resultados.append((nome_contrato, None))

    return resultados