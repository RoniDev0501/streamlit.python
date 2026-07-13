import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

modelo_ia = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

st.write('## Roni Chat')  # Markdown

if not 'lista_mensagens' in st.session_state:
    st.session_state['lista_mensagens'] = []

texto_usuario = st.chat_input('Digite sua mensagem aqui...')

for mensagem in st.session_state['lista_mensagens']:
    role = mensagem['role']
    content = mensagem['content']
    st.chat_message(role).write(content)

if texto_usuario:
    st.chat_message('user').write(texto_usuario)
    mensagem_usuario = {'role': 'user', 'content': texto_usuario}
    st.session_state['lista_mensagens'].append(mensagem_usuario)

    historico_formatado = []
    for m in st.session_state['lista_mensagens']:
        role_gemini = 'model' if m['role'] == 'assistant' else 'user'
        historico_formatado.append({'role': role_gemini, 'parts': [{'text': m['content']}]})

    resposta_ia = modelo_ia.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=historico_formatado,
    )   

    texto_resposta_ia = resposta_ia.text

    st.chat_message('assistant').write(texto_resposta_ia)
    mensagem_ia = {'role': 'assistant', 'content': texto_resposta_ia}
    st.session_state['lista_mensagens'].append(mensagem_ia)
