import time
import os
import json

import google.generativeai as genai
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity - Content Outline Generator",
        layout="wide",
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def title_and_description():
    st.title("🧕 Alwrity - AI Content Outline Generator")

def input_section():
    with st.expander("**PRO-TIP** - Better input yield, better results.", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            outline_title = st.text_input('**Enter Title of your content Or main keywords:**',
                        help="Describe the idea of whole content in a single sentence. Keep it between 1-3 sentences.",
                        placeholder="Input content topic Or title..")

            content_type = st.selectbox("Select the type of content:",
                    options=["Blog", "Article", "Essay", "Story", "Other"],
                    help="Choose the type of content you want to create an outline for.")
        with col2:
            num_headings = st.slider("Number of main headings:",
                             min_value=1,
                             max_value=10,
                             value=5,
                             help="Choose the number of main headings for the outline.")
    
            num_subheadings = st.slider("Number of subheadings per heading:",
                                min_value=1,
                                max_value=5,
                                value=3,
                                help="Choose the number of subheadings under each main heading.")
        
        if st.button('**Get AI Outline**'):
            if outline_title.strip():
                with st.spinner("Hang On, Generating Outline..."):
                    content_outline = generate_outline(outline_title, content_type, num_headings, num_subheadings)
                    if content_outline:
                        st.subheader('**👩🔬👩🔬 Your Content Outline:**')
                        st.markdown(content_outline)
                    else:
                        st.error("💥 **Failed to generate STAR copy. Please try again!**")
            else:
                st.error("Input Title/Topic of content to outline, Required!")



def generate_outline(outline_title, content_type, num_headings, num_subheadings):
    prompt = f"""As an expert & experienced content writer for various online platforms. I will provide you with my 'topic title'.
        You are tasked with outlining a {content_type}, type of content. 
        Your goal is to provide a well-structured content outline, with {num_headings} headings and {num_subheadings} subheadings.

        Follow the guideline below for writing the outline:

        1). Make sure, don’t follow any AI pattern but the title should be and informative.
        2). Do not use words that are too generic or words that have been used too many times before.
        3). Make sure to write {num_headings} headings and for each heading write {num_subheadings} subheadings.
        4). Think about the key sections, subsections, and points that need to be covered and ensure a smooth flow of ideas. 
        5). Make use of headings, subheadings, and bullet points to create a clear and coherent outline that serves as a roadmap for the content. 
        6). Be sure to proofread your outline, ensuring that it is well-written, without errors, and straightforward to follow.
        7). Do not explain what and why, just give me your finest possible Output.

        Important: Please read the entire prompt before writing anything, and do not do anything extra. 
        Follow the prompt exactly as I instructed. and use bold headings.

        \n\nMy 'topic title' is: '{outline_title}'

        """
    
    return gemini_text_response(prompt)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt):
    """ Common functiont to get response from gemini pro Text. """
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
    # Set up the model
    generation_config = {
        "temperature": 0.6,
        "top_p": 0.3,
        "top_k": 1,
        "max_output_tokens": 1024
    }
    # FIXME: Expose model_name in main_config
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", generation_config=generation_config)
    try:
        # text_response = []
        response = model.generate_content(prompt)
        return response.text
    except Exception as err:
        st.error(response)
        st.error(f"Failed to get response from Gemini: {err}. Retrying.")


if __name__ == "__main__":
    main()

