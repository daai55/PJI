import streamlit as st
import requests

# Adicionando estilo CSS
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        color: #4CAF50;
        text-align: center;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: None;
        padding: 10px 20px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">AgendAçougue</h1>', unsafe_allow_html=True)

api_url = " http://192.168.1.1:8501"

# Sessão de registro
st.header("Registrar-se")
nome = st.text_input("Nome", placeholder="Digite seu nome completo")
email = st.text_input("Email", placeholder="seu@email.com")
senha = st.text_input("Senha", type="password", placeholder="Escolha uma senha")

if st.button("Registrar"):
    response = requests.post(f"{api_url}/register", json={"nome": nome, "email": email, "senha": senha})
    if response.status_code == 200:
        st.success("Registro realizado com sucesso!", icon="✅")
    else:
        st.error("Erro no registro, tente novamente.", icon="❌")

# Sessão de login
st.header("Login")
login_email = st.text_input("Email para Login")
login_senha = st.text_input("Senha para Login", type="password")

if st.button("Login"):
    response = requests.post(f"{api_url}/login", json={"email": login_email, "senha": login_senha})
    if response.status_code == 200:
        token = response.json().get("token")
        st.success("Login realizado com sucesso!", icon="✅")
    else:
        st.error("Email ou senha incorretos.", icon="❌")

# Listar serviços disponíveis
if 'token' in locals():
    st.header("Serviços Disponíveis")
    response = requests.get(f"{api_url}/servicos")
    if response.status_code == 200:
        servicos = response.json().get("servicos", [])
        for servico in servicos:
            st.write(f"{servico['nome']}: {servico['descricao']} - R$ {servico['preco']} ({servico['duracao']} minutos)")
    else:
        st.error("Erro ao buscar serviços.")

# Agendamento de serviços
if 'token' in locals():
    st.header("Agendar Serviço")
    cliente_id = st.text_input("ID do Cliente")
    servico_id = st.text_input("ID do Serviço")
    data_hora = st.text_input("Data e Hora do Agendamento (YYYY-MM-DD HH:MM)")

    if st.button("Agendar"):
        response = requests.post(f"{api_url}/agendamentos", headers={"Authorization": f"Bearer {token}"}, json={
            "cliente_id": cliente_id,
            "servico_id": servico_id,
            "data_hora": data_hora
        })
        if response.status_code == 200:
            st.success("Agendamento realizado com sucesso!", icon="✅")
        else:
            st.error("Erro ao realizar agendamento.", icon="❌")
