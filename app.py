import streamlit as st
import time

from swarm import Swarm
from agent_pool import agent_gillie

client = Swarm()

st.set_page_config(page_title="Talk to Dezzi", page_icon="avatar/DSR.png")
st.title("🎓 Talk to Dezzi 📚")

gillie_avatar = "avatar/Dezzi2.png"
user_avatar = "avatar/user.png"

def response_generator(gen_response):
    for word in gen_response.split():
        yield word + " "
        #time.sleep(0.05)
        time.sleep(0.10)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """Hi there! 👋 I'm Dezzi, your personal expert in Design Science Research (DSR) 👨‍🏫.  
        Before we dive in, could you tell me about your current knowledge level of DSR?  
        Would you say you're a beginner just getting started, someone with some experience, or an advanced researcher? This will help me tailor my explanations to your needs! 😊"""}
    ]

# Display the chat messages so far
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar=gillie_avatar).write(msg["content"])
    elif msg["role"] == "user":
        st.chat_message(msg["role"], avatar=user_avatar).write(msg["content"])

# Get user input from Streamlit
if prompt := st.chat_input(placeholder="Reply to Dezzi"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=user_avatar).write(prompt)

    # Update `messages` with the conversation so far, to pass it to the agent
    messages = st.session_state.messages

    # Run the agent with the updated messages
    with st.spinner(text="Let me think about that..."):
        response = client.run(agent=agent_gillie, messages=messages)
    
    # Spinner stops as soon as the code block is finished
    agent_response = response.messages[-1]["content"]

    # Append the response to the session state messages and display it
    with st.chat_message("assistant", avatar=gillie_avatar):
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        st.write_stream(response_generator(agent_response))
