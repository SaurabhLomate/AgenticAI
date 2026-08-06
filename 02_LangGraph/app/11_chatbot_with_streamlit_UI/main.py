from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

model = ChatGroq(model = 'llama-3.1-8b-instant')

class MessageState(TypedDict) :
    messages : Annotated[list[BaseMessage], add_messages]
    
def chat(state: MessageState) :
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': response}

checkpointer = InMemorySaver()

graph = StateGraph(MessageState)
graph.add_node('chat', chat)
graph.add_edge(START, 'chat')
graph.add_edge('chat', END)

chatbot = graph.compile(checkpointer = checkpointer)

# thread_id = 1
# while True:
#     message = input('type message here')
#     if message.strip().lower() in ['exit', 'bye', 'quit']:
#         break
#     CONFIG = {'configurable':{'thread_id':thread_id}}
#     response = chatbot.invoke({'messages': HumanMessage(content= message)}, config = CONFIG)