from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from bs4 import BeautifulSoup
import datetime

class CearaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doc = request.query_params.get('doc', 'CNPJ')
        valor = request.query_params.get('valor', '00002224545000')

        if doc == "CNPJ":
            doc = 'cnpj_base'
        elif doc == "CPF":
            doc = 'cpf'

        response = self.consultar_divida(doc, valor)
        return Response(response.json())

    def consultar_divida(self, doc, valor):
        base_url = "https://apicontribuinte.pge.ce.gov.br/api/v1/divida_ativas/buscar_dividas"
        params = {'[buscar_dividas]documento': doc, '[buscar_dividas]valor': valor}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://portaldocontribuinte.pge.ce.gov.br/consulta',
            'X-Requested-With': 'XMLHttpRequest'
        }
        response = requests.get(base_url, params=params, headers=headers)
        return response

class PaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doc = request.query_params.get('doc', 'CNPJ')
        valor = request.query_params.get('valor', '04894085000150')

        if doc == "CNPJ":
            id = '2'
        elif doc == "CPF":
            id = '3'
        elif doc == "Inscrição":
            id = '4'
        else:
            return Response({"error": "Tipo de documento inválido"}, status=400)

        response = self.consultar_divida(id, valor)
        return Response(response.json())

    def consultar_divida(self, id, valor):
        url_base = "https://app.sefa.pa.gov.br/consulta-divida-ativa-api/api/consultarDivida"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'
        }
        params = {
            "identificacao": id,
            "textoIdentificacao": valor,
            "nome": None,
            "maioresDevedores": None,
            "foraEstado": False,
            "municipio": None,
            "natureza": None,
            "orgao": None,
            "protestada": False,
            "situacao": None,
            "tipoFiltro": "2"
        }
        response = requests.post(url_base, json=params, headers=headers, verify=False)
        return response

class PeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doc = request.query_params.get('doc', 'CNPJ')
        valor = request.query_params.get('valor', '13.481.309')

        if doc == "CNPJ":
            doc = "RADICAL_CNPJ"
        elif doc == "CPF":
            doc = "CPF"
        else:
            return Response({"error": "Tipo de documento inválido"}, status=400)

        response = self.consultar_divida(doc, valor)
        return Response(response)

    def consultar_divida(self, doc, valor):
        url = "https://efisco.sefaz.pe.gov.br/sfi_trb_gpf/PRConsultarDevedoresInscritosEmDividaAtiva"
        headers_get = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        session = requests.session()
        response = session.get(url, headers=headers_get)
        soup = BeautifulSoup(response.content, 'html.parser')

        id_sessao = soup.find('input', {'name': 'id_sessao'})['value']
        cookies = session.cookies.get_dict()
        cookies = cookies.get('JSESSIONID')
        data = datetime.date.today()
        data = data.strftime("%d/%m/%y")
        hora = datetime.datetime.now()
        hora = hora.strftime("%H:%M:%S")

        headers_post = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "1172",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"JSESSIONID={cookies}",
            "Host": "efisco.sefaz.pe.gov.br",
            "Origin": "https://efisco.sefaz.pe.gov.br",
            "Referer": "https://efisco.sefaz.pe.gov.br/sfi_trb_gpf/PRConsultarDevedoresInscritosEmDividaAtiva",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }

        payload = {
            "id_contexto_sessao": "",
            "evento": "processarFiltroConsulta",
            "nao_utilizar_id_contexto_sessao": "true",
            "ConsultaRealizada": None,
            "Flag": None,
            "id_sessao": id_sessao,
            "nm_path_servlet_anterior": "/sfi_trb_gpf/PRConsultarDevedoresInscritosEmDividaAtiva",
            "nm_path_jsp_anterior": "jsp/servico04/consultar_devedoresemda/p01consulta.jsp",
            "in_enderecodomicilio_valido": "",
            "cd_menu": "",
            "dt_hoje_framework": data,
            "hr_hoje_framework": hora,
            "cd_usuario": "1",
            "cd_tipo_usuario_sca": "",
            "historico": "",
            "nm_titulo_pagina": "",
            "in_janela_auxiliar": "",
            "in_formulario_submetido": "",
            "CdTipoDocumentoIdentificacao": doc,
            "CdTipoDocumentoIdentificacao_hidden": "",
            "NuDocumentoIdentificacao": valor,
            "NmRazaoSocial": "",
            "VlMaiorQueSaldo": "",
            "VlMenorQueSaldo": "",
            "qt_registros_pagina": "20"
        }

        response = session.post(url, data=payload, headers=headers_post)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find(id='table_tabeladados')
        rows = table.find_all('tr')

        total_valor = 0
        for row in rows[1:-1]:
            colunas = row.find_all('td')
            if colunas:
                
                dividas = colunas[0].get_text().strip()
                razao_social = colunas[1].get_text().strip()
                valor = colunas[3].get_text().strip()
                valor = float(valor.replace('.', '').replace(',', '.'))
                total_valor += valor

        resultado = {
            'dividas': dividas,
            'razao_social': razao_social,
            'valor': total_valor
        }

        return resultado