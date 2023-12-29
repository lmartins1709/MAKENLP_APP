import streamlit as st
from deep_translator import GoogleTranslator
from cachetools import LRUCache, cached
from generation import QuestionAnsweringModel
from summarization import summarize_text
from database import insert_data
import gc

# Crie um cache com um tamanho específico
translation_cache = LRUCache(maxsize=128)

# Função decorada com cache
@cached(cache=translation_cache)
def translate_text_cached(text, language):
    return GoogleTranslator(source='auto', target=language).translate(text)

# Carregue o modelo de linguagem uma vez fora da função
model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
qa_model = QuestionAnsweringModel(model_name)
qa_model.load_model()

def translate_page(language):
    translator = GoogleTranslator(source='auto', target=language)
    translated_title = translator.translate("Seja Bem Vindo ao MAKENLP")
    st.title(translated_title)
    translated_name = translator.translate("Nome:")
    name = st.text_input(translated_name)
    translated_age = translator.translate("Idade:")
    age = st.number_input(translated_age, step=1)
    translated_gender = translator.translate("Gênero:")
    gender_options = [translator.translate('Masculino'), translator.translate('Feminino')]
    gender = st.selectbox(translated_gender, options=gender_options)
    translated_text_input = translator.translate("Digite o texto para resumir:")
    st.subheader(translated_text_input)
    text_summarization = st.text_area("", height=150)
    if st.button(translator.translate("Resumir Texto")):
        summarized_text = summarize_text(text_summarization)
        st.subheader(translator.translate("Texto Resumido"))
        st.write(summarized_text)
    translated_text_gen = translator.translate("Digite o texto:")
    st.subheader(translated_text_gen)
    text_generation = st.text_area("", height=150, key='text_generation')
    translated_question = translator.translate("Faça uma pergunta sobre o texto:")
    question = st.text_input(translated_question, key='question')
    if st.button(translator.translate("Gerar Resposta")):
        answer = qa_model.generate_answer(question, text_generation)
        st.subheader(translator.translate("Resposta Gerada"))
        st.write(answer)
    translated_text_trans = translator.translate("Digite o texto para traduzir:")
    st.subheader(translated_text_trans)
    text_translation = st.text_area("", height=150, key='text_translation')
    translated_lang = translator.translate("Selecione o idioma de destino:")
    language_options = ['en', 'es', 'fr', 'pt']
    language = st.selectbox(translated_lang, options=language_options, key='language')
    if st.button(translator.translate("Traduzir Texto")):
        translated_text = translate_text_cached(text_translation, language)
        st.subheader(translator.translate("Texto Traduzido"))
        st.write(translated_text)
    if st.button(translator.translate("Enviar")):
        summarized_text = summarize_text(text_summarization)
        answer = qa_model.generate_answer(question, text_generation)
        translated_text = translate_text_cached(text_translation, language)
        insert_data(name, age, gender, text_summarization, summarized_text, text_generation,
                    question, answer, text_translation, language, translated_text)
        st.success(translator.translate("Dados inseridos com sucesso!"))

    # Liberar memória não utilizada
    gc.collect()

if __name__ == '__main__':
    st.set_page_config(page_title="MAKENLP", page_icon=":speech_balloon:")
    translation_language = st.selectbox("Selecione o idioma de tradução:", options=['pt', 'en', 'fr', 'es'])
    translate_page(translation_language)
