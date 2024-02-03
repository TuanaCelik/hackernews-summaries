
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown
import requests

import streamlit as st

from utils.haystack import query, start_haystack
from utils.ui import reset_results, set_initial_state, sidebar

set_initial_state()

sidebar()

def mistral_pressed():
    st.session_state["model"] = "Mistral"

def openai_pressed():
    st.session_state["model"] = "GPT-4"

st.write("# Get the summaries of latest top Hacker News posts 🧡")
if st.session_state.get("model") == None:
    mistral, openai = st.columns([2,1], gap="small")

    with mistral:
        st.button("Mixtral-8x7B-Instruct", on_click=mistral_pressed, type="primary")
        
    with openai:
        st.button("GPT-4", on_click=openai_pressed, type="primary")

if st.session_state.get("model") and (st.session_state.get("HF_TGI_TOKEN") or st.session_state.get("OPENAI_API_KEY")):
    
    if st.session_state.get("HF_TGI_TOKEN"):
        pipeline = start_haystack(st.session_state.get("HF_TGI_TOKEN"), st.session_state.get("model"))
        st.session_state["api_key_configured"] = True
    
    elif st.session_state.get("OPENAI_API_KEY"):
        pipeline = start_haystack(st.session_state.get("OPENAI_API_KEY"), st.session_state.get("model"))
        st.session_state["api_key_configured"] = True
    
    search_bar, button = st.columns(2)
    # Search bar
    with search_bar: 
        top_k = st.slider('How many of the top posts should I summarize?', 0, 5, 0)

    with button: 
        st.write("")
        st.write("")
        run_pressed = st.button("Get summaries")
elif st.session_state.get("model"):
    st.write("Please provide your Hugging Face or OpenAI key to start using the application")
    st.write("If you are using a smaller screen, open the sidebar from the top left to provide your token 🙌")
    
if st.session_state.get("api_key_configured"):
    run_query = (
        run_pressed or top_k != st.session_state.top_k
    )

    # Get results for query
    if run_query and top_k:
        reset_results()
        st.session_state.top_k = top_k
        with st.spinner("🔎"):
            try:
                st.session_state.result = query(top_k, pipeline)
            except JSONDecodeError as je:
                st.error(
                    "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
                )    
            except Exception as e:
                logging.exception(e)
                st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")            
                
    if st.session_state.result:
        summaries = st.session_state.result
        st.write(summaries[0])
            