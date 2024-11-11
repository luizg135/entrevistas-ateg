import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Carregar credenciais do Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/luiz.borato/Desktop/Docs/Entrevistas_ATeG_Credenciais.json', scope)
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
    # Verifica se o horário para a data já está ocupado
    return agendamentos[(agendamentos['Data'] == data) & (agendamentos['Horário'] == horario)].empty

def nome_disponivel(nome, agendamentos):
    # Verifica se o nome já foi usado para agendar
    return nome not in agendamentos['Nome'].values

def agendar_entrevista(data, horario, nome):
    # Recarregar os agendamentos para garantir dados atualizados
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
st.title('Agendamento de Entrevistas | ATeG')

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
        # Chamar a função de agendamento e confirmar se foi realizado
        if agendar_entrevista(data, horario, nome):
            # Recarregar a tabela para atualizar a interface com o novo agendamento
            agendamentos = carregar_agendamentos()