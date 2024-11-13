# import streamlit as st
# import pandas as pd
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import json
# import re

# # Título e ícone da aba
# st.set_page_config(page_title="Agenda ATeG", page_icon="🗓️")

# # Imagem de fundo
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), url("https://imgur.com/g2KWkEJ.png");
#         background-size: 50%;
#         background-position: center;
#         background-repeat: no-repeat;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Título, Caixa e Logo do Sistema FAEP
# st.markdown(
#     """
#     <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); display: flex; align-items: center; margin-bottom: 60px;">
#         <div style="flex: 1; text-align: left;">
#             <img src="https://imgur.com/ruDtZT7.png" width="150" style="margin-right: 10px;">
#         </div>
#         <div style="flex: 3; text-align: center;">
#             <h1 style="font-size: 50px; font-weight: bold; color: #235937; margin: 0;">Agenda ATeG</h1>
#             <h2 style="font-size: 20px; color: #000000; margin-top: -37px;">Agendamento de Entrevistas</h2>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Configuração do Google Sheets
# scope = ["https://spreadsheets.google.com/feeds", 
#          "https://www.googleapis.com/auth/spreadsheets", 
#          "https://www.googleapis.com/auth/drive.file", 
#          "https://www.googleapis.com/auth/drive"]

# # Função para validar o nome completo
# def validar_nome(nome):
#     padrao_nome = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:\s[A-Za-zÀ-ÖØ-öø-ÿ]+)+$"
#     return bool(re.match(padrao_nome, nome)) and len(nome) >= 5

# # Input de nome com validação
# nome = st.text_input('Digite seu nome: *')

# # Validação e aviso
# if nome and not validar_nome(nome):
#     st.error("Por favor, digite seu nome completo.")

# # Carregar as credenciais
# creds_json = st.secrets["google"]["GOOGLE_SHEET_CREDENTIALS_JSON"]

# if not creds_json:
#     st.error("Erro: As credenciais do Google não foram encontradas nas variáveis de ambiente.")
# else:
#     try:
#         creds_dict = json.loads(creds_json)
#         creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
#         client = gspread.authorize(creds)
#         spreadsheet = client.open("Agendamentos - ATeG")
#         sheet = spreadsheet.sheet1

#         datas = ['13/11/2024', '14/11/2024']
#         horarios_por_data = {
#             '13/11/2024': ['13h30', '14h00', '14h30', '15h00'],
#             '14/11/2024': ['15h30', '16h00', '16h30', '17h00']
#         }

#         def carregar_agendamentos():
#             try:
#                 agendamentos = pd.DataFrame(sheet.get_all_records())
#                 if not {'Data', 'Horário', 'Nome'}.issubset(agendamentos.columns):
#                     agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
#             except Exception as e:
#                 st.error(f"Erro ao carregar os agendamentos: {e}")
#                 agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
#             return agendamentos

#         def horario_disponivel(data, horario, agendamentos):
#             return agendamentos[(agendamentos['Data'] == data) & (agendamentos['Horário'] == horario)].empty

#         def nome_disponivel(nome, agendamentos):
#             return nome not in agendamentos['Nome'].values

#         def agendar_entrevista(data, horario, nome):
#             agendamentos = carregar_agendamentos()

#             if not horario_disponivel(data, horario, agendamentos):
#                 st.error(f'O horário {horario} no dia {data} já foi agendado!')
#                 return False
#             if not nome_disponivel(nome, agendamentos):
#                 st.error("Este nome já foi utilizado para agendamento. Por favor, insira um nome diferente.")
#                 return False

#             sheet.append_row([data, horario, nome])
#             st.success(f'Entrevista agendada com sucesso para {nome} no dia {data} às {horario}!')
#             return True

#         data = st.selectbox('Escolha a data: *', datas)

#         agendamentos = carregar_agendamentos()
#         horarios_disponiveis = [horario for horario in horarios_por_data[data] if horario_disponivel(data, horario, agendamentos)]

#         if not horarios_disponiveis:
#             st.warning("Todos os horários para esta data já foram agendados. Escolha outra data.")
#         else:
#             horario = st.selectbox('Escolha o horário: *', horarios_disponiveis)

#             if not nome.strip():
#                 st.warning("Por favor, preencha o campo 'Nome' para confirmar o agendamento.")
#             elif st.button('Confirmar Agendamento'):
#                 if validar_nome(nome) and agendar_entrevista(data, horario, nome):
#                     agendamentos = carregar_agendamentos()

#         st.markdown("<p style='color: red;'>* Campos de preenchimento obrigatório</p>", unsafe_allow_html=True)
        
#         # Campo de consulta de agendamento
#         st.markdown("---")
#         nome_busca = st.text_input("Digite seu nome para verificar o agendamento:", "")

#         if st.button("Pesquisar"):
#             if nome_busca:
#                 agendamentos_filtrados = agendamentos[agendamentos['Nome'].str.contains(nome_busca, case=False, na=False)]

#                 if agendamentos_filtrados.empty:
#                     st.info("Nenhum agendamento encontrado para o nome informado.")
#                 else:
#                     st.markdown(
#     """
#     <h3 style="font-size: 15px; color: #000000; font-weight: bold;">Agendamentos encontrados:</h3>
#     """,
#     unsafe_allow_html=True
# )

#                     for idx, row in agendamentos_filtrados.iterrows():
#                         st.markdown(
#                             f"""
#                             <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
#                                 <p><strong>Nome Completo:</strong> {row['Nome']}</p>
#                                 <p><strong>Data:</strong> {row['Data']}</p>
#                                 <p><strong>Horário:</strong> {row['Horário']}</p>
#                             </div>
#                             """, unsafe_allow_html=True)
#             else:
#                 st.warning("Digite um nome para buscar agendamentos.")

#     except Exception as e:
#         st.error(f"Erro ao configurar as credenciais ou acessar o Google Sheets: {e}")

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import re

# Título e ícone da aba
st.set_page_config(page_title="Agenda ATeG", page_icon="🗓️")

# Imagem de fundo
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), url("https://imgur.com/g2KWkEJ.png");
        background-size: 50%;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Título, Caixa e Logo do Sistema FAEP
st.markdown(
    """
    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); display: flex; align-items: center; margin-bottom: 60px;">
        <div style="flex: 1; text-align: left;">
            <img src="https://imgur.com/ruDtZT7.png" width="150" style="margin-right: 10px;">
        </div>
        <div style="flex: 3; text-align: center;">
            <h1 style="font-size: 50px; font-weight: bold; color: #235937; margin: 0;">Agenda ATeG</h1>
            <h2 style="font-size: 20px; color: #000000; margin-top: -37px;">Agendamento de Entrevistas</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Configuração do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Função para validar o nome completo
def validar_nome(nome):
    padrao_nome = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:\s[A-Za-zÀ-ÖØ-öø-ÿ]+)+$"
    return bool(re.match(padrao_nome, nome)) and len(nome) >= 5

# Input de nome com validação
nome = st.text_input('Digite seu nome: *')

# Validação e aviso
if nome and not validar_nome(nome):
    st.error("Por favor, digite seu nome completo.")

# Carregar as credenciais
creds_json = st.secrets["google"]["GOOGLE_SHEET_CREDENTIALS_JSON"]

if not creds_json:
    st.error("Erro: As credenciais do Google não foram encontradas nas variáveis de ambiente.")
else:
    try:
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("Agendamentos - ATeG")
        sheet = spreadsheet.sheet1

        datas = ['13/11/2024', '14/11/2024']
        horarios_por_data = {
            '13/11/2024': ['13h30', '14h00', '14h30', '15h00'],
            '14/11/2024': ['15h30', '16h00', '16h30', '17h00']
        }

        def carregar_agendamentos():
            try:
                agendamentos = pd.DataFrame(sheet.get_all_records())
                if not {'Data', 'Horário', 'Nome'}.issubset(agendamentos.columns):
                    agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
            except Exception as e:
                st.error(f"Erro ao carregar os agendamentos: {e}")
                agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
            return agendamentos

        def horario_disponivel(data, horario, agendamentos):
            return agendamentos[(agendamentos['Data'] == data) & (agendamentos['Horário'] == horario)].empty

        def nome_disponivel(nome, agendamentos):
            return nome not in agendamentos['Nome'].values

        def agendar_entrevista(data, horario, nome):
            agendamentos = carregar_agendamentos()

            if not horario_disponivel(data, horario, agendamentos):
                st.error(f'O horário {horario} no dia {data} já foi agendado!')
                return False
            if not nome_disponivel(nome, agendamentos):
                st.error("Este nome já foi utilizado para agendamento. Por favor, insira um nome diferente.")
                return False

            sheet.append_row([data, horario, nome])
            st.success(f'Entrevista agendada com sucesso para {nome} no dia {data} às {horario}!')
            return True

        data = st.selectbox('Escolha a data: *', datas)

        agendamentos = carregar_agendamentos()
        horarios_disponiveis = [horario for horario in horarios_por_data[data] if horario_disponivel(data, horario, agendamentos)]

        if not horarios_disponiveis:
            st.warning("Todos os horários para esta data já foram agendados. Escolha outra data.")
        else:
            horario = st.selectbox('Escolha o horário: *', horarios_disponiveis)

            if not nome.strip():
                st.warning("Por favor, preencha o campo 'Nome' para confirmar o agendamento.")
            elif st.button('Confirmar Agendamento'):
                if validar_nome(nome) and agendar_entrevista(data, horario, nome):
                    agendamentos = carregar_agendamentos()

        st.markdown("<p style='color: red;'>* Campos de preenchimento obrigatório</p>", unsafe_allow_html=True)

        # Campo de consulta de agendamento com uma separação visual discreta
        st.markdown("---")  # Linha para separar as seções

        st.markdown(
            """
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; margin-top: 30px;">
                <h3 style="font-size: 18px; color: #235937; font-weight: bold; text-align: center; margin-bottom: 10px;">Consultar Agendamento</h3>
                <p style="color: #666; text-align: center; margin-bottom: 20px;">Digite seu nome para verificar o agendamento</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Input para busca de agendamento
        nome_busca = st.text_input("Nome para consulta:", "")
        if st.button("Pesquisar"):
            if nome_busca:
                agendamentos_filtrados = agendamentos[agendamentos['Nome'].str.contains(nome_busca, case=False, na=False)]
                if agendamentos_filtrados.empty:
                    st.info("Nenhum agendamento encontrado para o nome informado.")
                else:
                    for idx, row in agendamentos_filtrados.iterrows():
                        st.markdown(
                            f"""
                            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <p><strong>Nome Completo:</strong> {row['Nome']}</p>
                                <p><strong>Data:</strong> {row['Data']}</p>
                                <p><strong>Horário:</strong> {row['Horário']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning("Digite um nome para buscar agendamentos.")

    except Exception as e:
        st.error(f"Erro ao configurar as credenciais ou acessar o Google Sheets: {e}")
