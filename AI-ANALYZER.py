import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os
from dotenv import load_dotenv
import openai

st.set_page_config(page_title="HDA", page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items=None)
# AI Analyzer Page
def ai_analyzer():
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
    
    st.markdown("""
    <nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
        <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
            <ul class="navbar-nav ">
                <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                    <a class="nav-link " href="#"><b> Medical Diagnostic AI-Analyzer </b><span class="sr-only">(current)</span></a>
                </li>
                <li>
                    <div>
                        <a href="https://chat.openai.com/c/12b8e7b5-491e-4353-b86b-af4e62c02fc6" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
    
    
    """, unsafe_allow_html=True)
    
    #<li class="nav-item">
    #                <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
    #            </li>
    
        
    
    # Set the theme colors
    st.markdown(
        """
        <style>
        :root {
            --primary-color: #B21F33;
            --background-color: 002b36;
            --secondary-background-color: #586e75;
            --text-color: #fafafa;
            --font: sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )        
    
    
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)
    
    
    
    
    hide_st_style = """
                <style>
                #MainMenu {visibility: visible;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
    
    
    
    
    lottie_coding = load_lottieurl("https://lottie.host/e8cca356-1ed3-4d6d-a263-377ffdbfae98/L1n9J2mGso.json")  # replace link to local lottie file
    
    
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    with st.sidebar:   
        selected = option_menu('',['AI-ANALYZER'],
                              icons=['person'],
                              default_index=0,
                              
                              )
        st_lottie(
                               lottie_coding,
                               speed=1,
                               reverse=False,
                               loop=True,
                               quality="low", # medium ; high
                               height="250px",
                               width="250px",
                               key=None,
                               )
        
    
        
    # Execute the code and display its output in the sidebar
    with st.sidebar:
        if selected == 'AI-ANALYZER':
    
    
    # Streamlit app title and description
    st.markdown("<h1 style='text-align: center;'>Medical Diagnostic AI-Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter patient information to receive a diagnostic recommendation</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    
    col1, col2, col3 = st.columns(3)
    
    # User inputs
    with col1:
        gender = st.radio("Gender", ["Male", "Female"])
    with col2:    
        pregnancy = st.radio("Pregnancy", ["No", "Yes"]) if gender == "Female" else "No"
    with col3:
        age = st.number_input("Age", min_value=0, max_value=99, step=1)
    
    context = st.text_input("Patient's Background (Example: gone to an outdoor music festival in north america, shared drinks and cigarettes with friends with similar symptoms)", value="none", max_chars=500 ,help="[Enter patient's known background information, including their past medical conditions, medications, family history, lifestyle, and other relevant information that can help in diagnosis and treatment]")
    symptoms = st.text_input("Symptoms (Example: high-grade fever, lethargy, headache, and abdominal pain for two days)", value="none", max_chars=500 ,help="[List all symptoms indicating the presence of an underlying medical condition]")
    exam_findings = st.text_input("Examination Findings (Example: petechial lesions on the palms of his hands and feet, bug bites)", value="none", max_chars=500, help="[List all the information gathered through visual inspection, palpation, percussion, and auscultation during the examination]")
    lab_results = st.text_input("Laboratory Test Results (Example: w/IgE levels > 3000 IU/m)", value="none", max_chars=500, help="[List output of tests performed on samples of bodily fluids, tissues, or other substances to help diagnose, monitor, or treat medical conditions. These tests can include blood tests, urine tests, imaging tests, biopsies, and other diagnostic procedures]")
    
    # Combine user inputs into a report
    report_list = [
        f"Gender: {gender}",
        f"Age: {age}",
        f"Pregnancy: {pregnancy}" if gender == "Female" else "",
        context,
        symptoms,
        exam_findings,
        lab_results
    ]
    report = "\n".join([f"{i + 1}. {report_list[i]}" for i in range(len(report_list)) if report_list[i] != "none"])
    
    # Button to trigger the diagnostic analysis
    if st.button("Analyze"):
        if symptoms != "none":
            # Add a spinner while generating the diagnostic recommendation
            with st.spinner("Generating diagnostic details..."):
                # Make API call to OpenAI
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use Codex engine for code-based tasks
                    prompt=f"Patient with the following information:\n\n{report}\n\nProvide diagnostic name, precautions and a large brief explanation about the found diagnostic.",
                    max_tokens=300
                )
    
            # Display the diagnostic recommendation
            st.subheader("Predicted Diagnostic Details:")
            st.write(response["choices"][0]["text"])
    
            # Display a note
            st.markdown("---")
            st.info(
                "Disclaimer: The diagnostic recommendation provided here is generated based on the information provided "
                "and is not a substitute for professional medical advice. It is important to note that this system does not "
                "guarantee 100% accuracy. Consultation with a qualified healthcare professional is strongly recommended for "
                "a precise and reliable diagnosis. Your health and well-being are of utmost importance, and a medical expert "
                "can provide personalized guidance based on a thorough examination of your specific situation."
            )
            st.markdown("---")
        else:
            st.warning("Please enter symptoms before analyzing.")


# Medical Chatbot Page
def medical_chatbot():
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
    
    st.markdown("""
    <nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
        <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
            <ul class="navbar-nav ">
                <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                    <a class="nav-link " href="#"><b> Medical Chatbot </b><span class="sr-only">(current)</span></a>
                </li>
                <li>
                    <div>
                        <a href="https://chat.openai.com/c/12b8e7b5-491e-4353-b86b-af4e62c02fc6" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
    
    
    """, unsafe_allow_html=True)
    
    #<li class="nav-item">
    #                <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
    #            </li>
    
        
    
    # Set the theme colors
    st.markdown(
        """
        <style>
        :root {
            --primary-color: #B21F33;
            --background-color: 002b36;
            --secondary-background-color: #586e75;
            --text-color: #fafafa;
            --font: sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )        
    
    
    reduce_header_height_style = """
        <style>
            div.block-container {padding-top:0rem;}
        </style>
    """
    st.markdown(reduce_header_height_style, unsafe_allow_html=True)
    
    
    
    
    hide_st_style = """
                <style>
                #MainMenu {visibility: visible;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
    
    
    
    
    lottie_coding = load_lottieurl("https://lottie.host/e8cca356-1ed3-4d6d-a263-377ffdbfae98/L1n9J2mGso.json")  # replace link to local lottie file
    
    
    with st.sidebar:   
        selected = option_menu('',['MEDICAL-CHATBOT'],
                              icons=['person'],
                              default_index=0,
                              
                              )
        st_lottie(
                               lottie_coding,
                               speed=1,
                               reverse=False,
                               loop=True,
                               quality="low", # medium ; high
                               height="250px",
                               width="250px",
                               key=None,
                               )
            
    
    
 
    # Execute the code and display its output in the sidebar
    with st.sidebar:
        if selected == 'MEDICAL-CHATBOT':

    def get_initial_message():
        messages=[
                {"role": "system", "content": "You are a helpful Medical Diagnostic AI Doctor. Who anwers brief questions about Diseases, Symptomps and medical findings."},
                {"role": "user", "content": "I want to know about my disease"},
                {"role": "assistant", "content": "Thats awesome, what do you want to know about medical conditions"}
            ]
        return messages
    
    def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
        print("model: ", model)
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages
        )
        return  response['choices'][0]['message']['content']
    
    def update_chat(messages, role, content):
        messages.append({"role": role, "content": content})
        return messages
    # Function to update and display response
    def update_and_display_response(query, model):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
    
    # Function to display chat history
    def display_chat_history():
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
    
    # Load environment variables
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    
    st.markdown("<h1 style='text-align: center;'>Medical Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Ask Medical-Related Questions:")
    
    # ChatGPT Model selection
    model = st.selectbox("ChatGPT Model", ("gpt-3.5-turbo",))
    
    # Initialize session state if not present
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message()
    
    # Default medical prompt
    query = st.text_input("Ask a medical question: ", key="input", value="What are the symptoms of a common cold?")
    
    # Check if there's a default query and generate response on app start
    if query and 'generated' not in st.session_state:
        update_and_display_response(query, model)
    
    # Handle user input and generate response
    if query:
        with st.spinner("Generating response..."):
            update_and_display_response(query, model)
    
    # Display chat history
    if st.session_state['generated']:
        display_chat_history()


# Sidebar navigation menu
selected_page = st.sidebar.radio("Select Page", ["AI Analyzer", "Medical Chatbot"])

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Display the selected page based on user choice
if selected_page == "AI Analyzer":
    ai_analyzer()
elif selected_page == "Medical Chatbot":
    medical_chatbot()
