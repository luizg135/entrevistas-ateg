import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

import streamlit as st

# Configura o título e o ícone da aba
st.set_page_config(
    page_title="Agenda ATeG",  # Título da aba
    page_icon="🗓️"  # Ícone da aba, pode ser um emoji ou o caminho de uma imagem .png
)

# CSS para adicionar a imagem de fundo
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://imgur.com/Mmj3g7Z.png");  /* Coloque o link direto aqui */
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); display: flex; align-items: center; margin-bottom: 60px;">
        <div style="flex: 1; text-align: left;">
            <img src="https://imgur.com/ruDtZT7.png" width="150" style="margin-right: 10px;">
        </div>
        <div style="flex: 3; text-align: center;">
            <h1 style="font-size: 50px; font-weight: bold; color: #235937; margin: 0;">Agenda ATeG</h1>
            <h2 style="font-size: 20px; color: #000000; margin-top: -35px;">Agendamento de Entrevistas</h2>
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

# Carregar as credenciais do Google Sheets a partir do Streamlit Secrets
creds_json = st.secrets["google"]["GOOGLE_SHEET_CREDENTIALS_JSON"]

# Se as credenciais não estiverem configuradas corretamente, exibe erro
if not creds_json:
    st.error("Erro: As credenciais do Google não foram encontradas nas variáveis de ambiente.")
else:
    try:
        # Carregar credenciais usando o JSON passado pelo Streamlit secrets
        creds_dict = json.loads(creds_json)  # Convertendo de JSON para dicionário
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Abrir a planilha pelo ID ou nome
        spreadsheet = client.open("Agendamentos - ATeG")
        sheet = spreadsheet.sheet1  # ou selecione pelo nome da aba

        # Definir datas e horários disponíveis
        datas = ['13/11/2024', '14/11/2024']
        horarios = ['13h30', '14h00', '14h30', '15h00', '15h30', '16h00', '16h30', '17h00']

        # Função para recarregar os dados de agendamentos do Google Sheets
        def carregar_agendamentos():
            try:
                agendamentos = pd.DataFrame(sheet.get_all_records())
                if not {'Data', 'Horário', 'Nome'}.issubset(agendamentos.columns):
                    agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
            except Exception as e:
                st.error(f"Erro ao carregar os agendamentos: {e}")
                agendamentos = pd.DataFrame(columns=['Data', 'Horário', 'Nome'])
            return agendamentos

        # Funções de validação e agendamento
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

            # Adicionar o novo agendamento
            sheet.append_row([data, horario, nome])
            st.success(f'Entrevista agendada com sucesso para {nome} no dia {data} às {horario}!')
            return True

        # Interface Streamlit
        # st.title('Agendamento de Entrevistas | ATeG')

        # Formulário de agendamento
        nome = st.text_input('Digite seu nome:')
        data = st.selectbox('Escolha a data:', datas)

        # Recarregar os agendamentos para garantir a atualização
        agendamentos = carregar_agendamentos()

        # Filtrar horários disponíveis para a data selecionada
        horarios_disponiveis = [horario for horario in horarios if horario_disponivel(data, horario, agendamentos)]
        if not horarios_disponiveis:
            st.warning("Todos os horários para esta data já foram agendados. Escolha outra data.")
        else:
            horario = st.selectbox('Escolha o horário:', horarios_disponiveis)

            # Verificar se a data, horário e nome estão disponíveis
            if not nome.strip():
                st.warning("Por favor, preencha o campo 'Nome' para confirmar o agendamento.")
            elif st.button('Confirmar Agendamento'):
                if agendar_entrevista(data, horario, nome):
                    agendamentos = carregar_agendamentos()  # Recarregar para atualizar a lista de agendamentos

    except Exception as e:
        st.error(f"Erro ao configurar as credenciais ou acessar o Google Sheets: {e}")
