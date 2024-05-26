import json  # JSON Parsing
import requests  # Import requests library to request HTTP
import streamlit as st  # Import Streamlit library

# Define Endpoint of AWS Lambda function URL
ENDPOINT_LAMBDA_URL = "https://3xpms6ntpkz2ttix2upww3inta0ynvbx.lambda-url.us-east-1.on.aws/"
    
# App title
st.title("💬 Chatbot powered by Amazon Bedrock")
st.caption("🚀 Tech Stack: Streamlit, AWS Lambda, Amazon EC2, AWS Cloud9")

# Reset if there is no messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Loop in the message in session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])  # Markdown the content of the message

def get_streaming_response(prompt):
    s = requests.Session()
    response = s.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt}, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            json_data = json.loads(chunk.decode())  # Parse the JSON data
            if 'output' in json_data:
                text = json_data['output']  # Extract the text under the 'output' key
                print(text)
                yield text

# Input from users
if prompt := st.chat_input("Message Bedrock..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  
        st.markdown(prompt)  # Markdown user messanges

    with st.chat_message("assistant"):  
        model_output = st.write_stream(get_streaming_response(prompt))

    # Assistant message
    st.session_state.messages.append({"role": "assistant", "content": model_output})
