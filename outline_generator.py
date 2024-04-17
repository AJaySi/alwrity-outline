import time
import os
import json
import openai
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
    with st.expander("**How to Use** Alwrity AI content outline Generator? 📝❗"):
        st.markdown('''
           ---
		**Step 1: Open the Streamlit App**
		
		Access the Streamlit app where the tool is deployed.
		
		**Step 2: Input Title and Select Content Type**
		
		In the first input field labeled **"Enter Title of your content Or main keywords:"**, type a descriptive title or main keywords summarizing the content you want to create an outline for.
		
		Then, select the type of content you're outlining from the dropdown menu labeled **"Select the type of content:"**. Choose from options such as Blog, Article, Essay, Story, or Other.
		
		**Step 3: Specify Outline Details**
		
		After entering the title and selecting the content type, adjust the sliders to specify the number of main headings and subheadings per heading.
		
		- Use the slider labeled **"Number of main headings:"** to select how many main sections you want in your outline.
		- Similarly, use the slider labeled **"Number of subheadings per heading:"** to choose the number of subsections under each main section.
		
		**Step 4: Generate Outline**
		
		Once you've provided the necessary details, click the "Generate Outline" button.
		
		**Step 5: Review and Utilize the Outline**
		
		After the outline is generated, review it to ensure it aligns with your expectations and serves as a structured framework for your content.
		
		**Step 6: Further Editing (If Necessary)**
		
		If needed, make adjustments to the generated outline or refine it according to your preferences.
		
		**Step 7: Save or Export the Outline**
		
		Once satisfied with the outline, save or export it
 
            ---
        ''')


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

    page_bottom()


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
    
    return openai_chatgpt(prompt)


def page_bottom():
    """Display the bottom section of the web app."""
    with st.expander("Alwrity - Content outline generator - powered by AI (OpenAI, Gemini Pro)."):
        st.write('''
        Introducing Alwrity - Your Ultimate Content Outline AI Generator!

			Are you struggling to structure your content effectively? Say goodbye to writer's block and endless brainstorming sessions with Alwrity - the AI-powered Content Outline Generator!
			
			**🧠 Unlock Creativity:** Alwrity leverages cutting-edge AI technology to generate well-organized, logically structured outlines for your content, whether it's a blog post, article, essay, or story.
			
			**🚀 Seamless Workflow:** With just a few clicks, you can input your content title, select the type of content you're creating, and specify the number of headings and subheadings. Alwrity takes care of the rest, providing you with a detailed outline in seconds.
			
			**📝 How It Works:**
			1. **Input Title & Select Content Type:** Describe your content idea in a single sentence and choose from various content types.
			2. **Specify Outline Details:** Customize the number of main headings and subheadings to tailor the outline to your needs.
			3. **Generate Outline:** Click the button, and Alwrity will swiftly generate a structured outline based on your inputs.
			4. **Review & Edit:** Review the outline, make any necessary adjustments, and fine-tune it to perfection.
			5. **Save or Export:** Once satisfied, save or export the outline to kickstart your content creation journey.
			
			**💡 Pro Tips:** For better results, provide detailed input and follow the guidelines provided within the tool.
			
			Say hello to hassle-free content creation with Alwrity - Your trusted partner for crafting compelling content outlines effortlessly. Try it now and unleash your creativity like never before!
			
			[Get Started Now](https://alwrity.com)
			
			---
			
			Content outline generator - powered by AI (OpenAI, Gemini Pro).	
			Implemented by [Alwrity](https://alwrity.com).
        ''')



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=1500, top_p=0.6, n=3):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")



if __name__ == "__main__":
    main()

