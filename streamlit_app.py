import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI

template = """
    A continuación tienes una idea para un libro que me gustaria que me escribieras una pagina.
    Tu objetivo es:
    - Redactar de forma atractiva para un libro infantil
    - Convierte el draft text para la edad especifica
    - Traduce el draft text al idioma especifico.

    Aqui tienes un ejemplo de redacción para edades:
    - 3 años: Cuando el agua se va y se convierte en nubes en el cielo, eso se llama evaporación
    - 6 años: ¡La evaporación es como magia! Es cuando el agua se calienta tanto que desaparece y se convierte en vapor invisible que sube al aire.  

    Here are some examples of words in different languages:
    - Català: burru, taula, cadira, forquilla
    - Castellano: tonto, mesa, silla, tenedor


    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, edad, and language:
    DRAFT: {draft}
    EDAD: {edad}
    LANGUAGE: {language}

    YOUR {language} RESPONSE:
"""
#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["edad", "language", "draft"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="write your idea")
st.header("Re-write your idea Mia")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Re-write your text for different ages.")

with col2:
    st.write("Contact with [mosquitos](https://mosquitobooksbarcelona.com/) to build your Ideas")


#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Enter your idea you want to write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_edad = st.selectbox(
        'Que edad tiene el cabroncete que va a leer el libro',
        ('3 años', '6 años'))
    
with col2:
    option_language = st.selectbox(
        'En que idioma quieres el libro?',
        ('Català', 'Castellano'))
    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        edad=option_edad, 
        language=option_language, 
        draft=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    st.write(improved_redaction)
