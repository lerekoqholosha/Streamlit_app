import openai
import streamlit as st
import re
import sys
import subprocess
import os
import nbformat

# Set up Streamlit sidebar
with st.sidebar:
    st.title('🤖💬 SmartAnalysis App')
    
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
            # subprocess.run(["python", "fdf.py"], check=True)


# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and process with OpenAI model
if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages],
                stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        vv = full_response.partition(":")[2].split('In')[0]
        
        ##Extract code from the full_response
        extracted_code = re.search(r'```(.*?)```', full_response, re.DOTALL)
        if extracted_code:
           code = extracted_code.group(1)
        st.code(code)  # Display extracted code

    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    vv = full_response.partition(":")[2].split('In')[0]
        
    st.markdown(vv)
    with open("fdf.py", "w") as file:
        file.write(code)
        file.close()
     #file.close()

    #  from PIL import Image

    #  image = Image.open(r"image.png")

    #  image.show() 

with open('fdf.py','r') as f:
    newlines = []
    for line in f: 
        if "plt.show()" in line:
            newlines.append(line.replace('python', "")) 
        else:   
            newlines.append(line) 
with open('fdf.py', 'w') as f: 
    for line in newlines:   
        f.write(line)
        f.close()

subprocess.run([f"{sys.executable}","fdf.py"], check=True,shell=True,stderr=subprocess.STDOUT)

