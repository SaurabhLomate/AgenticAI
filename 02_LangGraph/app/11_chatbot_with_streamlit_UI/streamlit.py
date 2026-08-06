import streamlit as st
from main import chatbot
from langchain_core.messages import HumanMessage

thread_id = 1
CONFIG = {'configurable':{'thread_id':thread_id}}
    
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
# {'role':'user/assistant', 'content':'respose'}

for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])
            
user_input =  st.chat_input('say something')

if user_input :
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    # response = chatbot.invoke({
    #     'messages': HumanMessage(user_input)
    # }, config= CONFIG)
    # ai_msg = response['messages'][-1].content
    # st.session_state['message_history'].append({'role':'assistant', 'content':ai_msg})
    # with st.chat_message('assistant'):
    #     st.text(ai_msg)
    
    ai_message = st.write_stream(
        message_chunk.content for message_chunk, metadata in chatbot.stream(
                    {'messages':HumanMessage(content= user_input)}, 
                    config = CONFIG, 
                    stream_mode = 'messages'))
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})