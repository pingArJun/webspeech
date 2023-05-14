import streamlit as st
from transformers import pipeline

# Load the OpenAI GPT-3 model
nlp = pipeline('text-generation', model='gpt-3')

st.title('AI Assistant')

# Add voice input and output
st.write('''
    <label for="voice-input">Say something:</label>
    <input id="voice-input" type="text" size="50">
    <script>
        const voiceInput = document.querySelector('#voice-input');
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            voiceInput.value = transcript;
            voiceInput.dispatchEvent(new Event('change'));
        }
        voiceInput.onclick = () => {
            recognition.start();
        }
    </script>
''', unsafe_allow_html=True)

# Get user input
user_input = st.text_input('Enter your message:')

# Generate response
if user_input:
    response = nlp(user_input, max_length=100)[0]['generated_text']
    st.write(response)
    st.write(f'''
        <script>
            const utterance = new SpeechSynthesisUtterance('{response}');
            speechSynthesis.speak(utterance);
        </script>
    ''', unsafe_allow_html=True)

# Add interactive widgets
st.sidebar.header('Settings')
max_length = st.sidebar.slider('Max response length', 10, 500, 100)
model = st.sidebar.selectbox('Model', ['gpt-3', 'gpt-2'])

# Update the model and max_length based on user input
nlp = pipeline('text-generation', model=model)
if user_input:
    response = nlp(user_input, max_length=max_length)[0]['generated_text']
    st.write(response)
