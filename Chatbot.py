import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.memory.buffer import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv 


load_dotenv()


if "GROQ_API_KEY" not in os.environ:
    st.error("No GROQ_API_KEY found. Please add it to your .env file.")
    st.stop()


@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

llm = get_llm()


if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   

st.title("Simple Chatbot")
st.markdown("You can choose the persona fromthe following drop down box : ")
persona = st.selectbox("Choose persona - ", ["Default", "RoastBot", "ShakespeareBot", "EmojiBot"])

with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input("You:", key="user_input")
    submit_clicked = st.form_submit_button("Send")

PERSONA_PROMPTS = {
    "Default": "You are a helpful assistant.",
    "RoastBot": "You are RoastBot. Always answer with witty, light-hearted roasts. Keep it funny, not abusive.",
    "ShakespeareBot": "You are ShakespeareBot. Reply in Shakespeare-style Early Modern English (thee, thou, thy), poetic and old-English.",
    "EmojiBot": "You are EmojiBot. Convert user messages into emoji-only 'emoji-speak' as clearly as possible."
}

def memory_to_messages(mem):
    """
    Convert mem.buffer_as_messages (LangChain message objects)
    into a list of message objects suitable for llm.invoke([...]).
    """
   
    return list(mem.buffer_as_messages)


if submit_clicked and user_text:
    
    system_msg = SystemMessage(content=PERSONA_PROMPTS.get(persona, PERSONA_PROMPTS["Default"]))
    history_msgs = memory_to_messages(st.session_state.memory)
    messages = [system_msg] + history_msgs + [HumanMessage(content=user_text)]

   
    ai_response = llm.invoke(messages)   
    ai_text = ai_response.content

    
    st.session_state.chat_history.append(("You", user_text))
    st.session_state.chat_history.append(("Bot", ai_text))

    
    st.session_state.memory.save_context({"input": user_text}, {"output": ai_text})

for speaker, text in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Bot:** {text}")

if st.button("Reset conversation"):
    st.session_state.memory.clear()            # clear the ConversationBufferMemory
    st.session_state.chat_history = []
    st.success("Conversation cleared.")


