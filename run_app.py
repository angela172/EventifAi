from helper import *
import mysql.connector
from googleapiclient.discovery import build
from langchain_community.llms import Ollama
logger = logging.getLogger()
import streamlit as st
from langchain_community.llms import Ollama
import pandas as pd
from app_helper import *
from email_tester_testing import *

def main():
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    # os.environ["OPENAI_API_KEY"] = config["openai_key"]
    # ☝️ To be replaced with Llama or any other way tp retreive API key
    
    logging.basicConfig(
        format="%(message)s",
        handlers=[logging.StreamHandler(ColorPrint())],
    )
    logger.setLevel(logging.INFO)
    api_spec, headers = None, None

    # # database connection details
    # db_config = {
    #     'host': 'localhost',
    #     'database': 'synapse-copilot',
    #     'user': 'root',
    #     'password': '2021A7PS0183U',
    # }

    # # Connect to the MySQL server
    # conn = mysql.connector.connect(**db_config)
    # cursor = conn.cursor()

    api_key = config["google_calendar"]["api_key"]
    creds_path = config["google_calendar"]["creds_path"]
    token_path = config["google_calendar"]["token_path"]
    
    #...
    # api_key = config["google_calendar"]["api_key"]
    # creds_path = config["google_calendar"]["creds_path"]
    # token_path = config["google_calendar"]["token_path"]

    # # Get Google Calendar service
    # service = get_google_calendar_service(creds_path, token_path)
    #...
    
    #The Streamlit App
    
    # Custom CSS for styling including gradient background
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
        body {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: transparent;
        }
        .title1 {
            font-family: 'Poppins', sans-serif;
            font-size: 3.5em;
            color: #ffffff;
            text-align: center;
            margin-top: 20px;
            layout="wide";
        }
        .title2 {
            font-family: 'Poppins', sans-serif;
            font-size: 6em;
            text-align: center;
            margin-top: 10px;
            layout="wide";
            background: linear-gradient(90deg, #9a2e6a, #ec4a59);
            -webkit-background-clip: text;
            color: transparent;
        }
        .subtitle {
            font-size: 1.5em;
            color: #ec8740;
            text-align: center;
            margin-bottom: 40px
            layout="wide";
        }
        .intro-text {
            font-size: 2em;
            color: #ffffff;
            text-align: center;
            width: 100%;
            margin: 20px auto;
        }
        .get-started {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .header {
            text-align: center;
            color: #61dafb;
        }
        .button {
            background-color: #61dafb;
            color: #282c34;
            border: none;
            padding: 10px 20px;
            font-size: 2em;
            cursor: pointer;
            border-radius: 5px;
            text-align: center;
            display: inline-block;
            margin: 20px 10px;
            text-decoration: none;
        }
        .button:hover {
            background-color: #21a1f1;
        }
        .centered-button {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
        }
        .file-upload {
            color: #ffffff;
        }
        .stApp {
            background-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    # Setting the background image
    page_bg_img = '''
    <style>
    .stApp {
    background: linear-gradient(to right, #061a23, #061a23);
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Ensure 'page' in st.session_state is set
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Home'

    # Check the current page
    page = st.session_state['page']

    # Title of the app
    st.markdown('<div class="title1">Welcome to our app </div>', unsafe_allow_html=True)
    st.markdown('<div class="title2">EventifAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">YOUR EVENTFUL FUTURE MADE EASY</div>', unsafe_allow_html=True)

    if page == "Home":
        # Home page content
        st.markdown('<div class="intro-text">Your one-stop app for scheduling Google Calendar events, adding participants, and sending personalized emails... all powered by AI!🦙</div>', unsafe_allow_html=True)
        st.image('logo.jpeg', use_column_width=True)
        if st.button("Get Started!"):
            st.session_state.page = "Event Planner"
            st.experimental_rerun()
                
    #Plan Events
    if page == "Event Planner":
        # Ensure session_state for event_type
        if 'event_type' not in st.session_state:
            st.session_state['event_type'] = None

        # Event type selection page
        if st.session_state['event_type'] is None:
            st.header("Select Event Type")
            event_type = st.radio("Is the event onsite or online?", ("Onsite Event", "Online Event"), key="event_type_radio")

            if st.button("Next"):
                st.session_state['event_type'] = event_type
                st.experimental_rerun()

        # 💻 Details for online events
        if st.session_state['event_type'] is not None:
            if st.session_state.get('event_type') == "Online Event":
                st.title("💻 Online Event Planner")

                if 'file_uploaded' not in st.session_state:
                    st.session_state['file_uploaded'] = False
                if 'emails' not in st.session_state:
                    st.session_state['emails'] = None
                if 'event_created' not in st.session_state:
                    st.session_state['event_created'] = False    
                
                st.header("Upload Guest/Participant list")
                email_uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

                if email_uploaded_file is not None:
                    st.session_state['file_uploaded'] = True
                    st.session_state['uploaded_data'] = pd.read_excel(email_uploaded_file)
                    st.success("Excel file uploaded successfully!")
                    emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
                    if emails:
                        st.session_state['emails'] = emails  # Store emails in session state
                        st.write("Extracted Emails:")
                        
                    else:
                        st.error("No emails found in the 'user_email' column.")
                    st.dataframe(st.session_state['uploaded_data'])
                
                    # api_key = config["google_calendar"]["api_key"]
                    # creds_path = config["google_calendar"]["creds_path"]
                    # token_path = config["google_calendar"]["token_path"]

                with st.spinner("Cooking Something 🍔..."):
                # Get Google Calendar service
                    service = get_google_calendar_service(creds_path, token_path)
                    
                prompt = st.text_input("Type your prompt here (don't forget to mention the date and time and location!): ")
                
                if st.button("OK") and not st.session_state['event_created']:
                    with st.spinner("Cooking Something 🍔..."):
                        changed_prompt = event_chatbot(emails, prompt)
                        
                        event_details = format_event_response(changed_prompt)
                        
                        st.session_state['event_details'] = event_details
                        
                        
                if st.button("Add to Calendar"):
                    
                    if st.session_state['event_details']:
                        
                        with st.spinner("Cooking Something 🍔..."):
                        # Create the event
                            event_response = create_google_calendar_event(service, st.session_state['event_details'], True)
                            # st.write(event_response)
                            event_link = event_response.get('htmlLink')
                            meet_link = event_response.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri')
                            
                            st.success("Event created successfully!")
                            st.session_state['event_created'] = True
            
                            if event_link:
                                st.markdown(f"[Google Calendar Event Link]({event_link})")
                            if meet_link:
                                st.markdown(f"[Google Meet Link]({meet_link})")
                        
                        # if st.session_state['event_created']:
                        #     st.success("Event already created. Refresh the page to create a new event.")    
                            
                        populate_api_selector_icl_examples()
                        populate_planner_icl_examples()

                        requests_wrapper = Requests(headers=headers)

                        llm = Ollama(model="llama3", temperature=0.0)
        
        #🌍 Details page for onsite events
        if st.session_state['event_type'] is not None:
            if st.session_state.get('event_type') == "Onsite Event":
                st.title("Onsite Event Planner")
                
                
                if st.button("Calendar Automation"):
                    st.session_state['page'] = 'Calendar'
                    st.experimental_rerun()
                if st.button("Email Invite Automation"):
                    st.session_state['page'] = 'Email_Invite'
                    st.experimental_rerun()
                    
    if st.session_state['page'] == 'Calendar':             
            st.title("📆 Schedule Calendar Events:")
            
            if 'page' not in st.session_state:
                st.session_state['page'] = 'Calendar'
            if 'file_uploaded' not in st.session_state:
                st.session_state['file_uploaded'] = False
            if 'emails' not in st.session_state:
                st.session_state['emails'] = None
            if 'event_created' not in st.session_state:
                st.session_state['event_created'] = False    
            
            st.header("Upload Guest/Participant list")
            email_uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

            if email_uploaded_file is not None:
                st.session_state['file_uploaded'] = True
                st.session_state['uploaded_data'] = pd.read_excel(email_uploaded_file)
                st.success("Excel file uploaded successfully!")
                emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
                if emails:
                    st.session_state['emails'] = emails  # Store emails in session state
                    st.write("Extracted Emails:")
                    
                else:
                    st.error("No emails found in the 'user_email' column.")
                st.dataframe(st.session_state['uploaded_data'])
            
    
                

            with st.spinner("Cooking Something 🍔..."):
            # Get Google Calendar service
                service = get_google_calendar_service(creds_path, token_path)
                
            prompt = st.text_input("Type your prompt here (don't forget to mention the date and time and location!): ")
            
            if st.button("OK") and not st.session_state['event_created']:
                with st.spinner("Cooking Something 🍔..."):
                    changed_prompt = event_chatbot(emails, prompt)
                    st.write(emails)
                    event_details = format_event_response(changed_prompt)
                    
                    st.session_state['event_details'] = event_details
                    
            if st.button("Add to Calendar"):
                
                if st.session_state['event_details']:
                    
                    with st.spinner("Cooking Something 🍔..."):
                    # Create the event
                        event_response = create_google_calendar_event(service, st.session_state['event_details'], False)
                        event_link = event_response.get('htmlLink')
                        st.success("Event created successfully!")
                        st.session_state['event_created'] = True
        
                        if event_link:
                            st.markdown(f"[Google Calendar Event Link]({event_link})")
                    
                    # if st.session_state['event_created']:
                    #     st.success("Event already created. Refresh the page to create a new event.")    
                        
                    populate_api_selector_icl_examples()
                    populate_planner_icl_examples()

                    requests_wrapper = Requests(headers=headers)

                    llm = Ollama(model="llama3", temperature=0.0)

                    
    if st.session_state['page'] == 'Email_Invite':    
        st.title("📧 Email Template Generator")

        if "email_template" not in st.session_state:
            st.session_state.email_template = ""
        if "attachment" not in st.session_state:
            st.session_state.attachment = None
        if "attachment_name" not in st.session_state:
            st.session_state.attachment_name = None

        event_type = st.text_input("Enter the type of event:")

        tone = st.radio("Choose the tone of the email:", ("formal", "informal"))
        name = st.text_input("Enter your name:")
        prompt = st.text_input("Type your prompt here (don't forget to mention the date and time!): ")

        st.header("Upload Guest/Participant list")
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

        if uploaded_file is not None:
            st.session_state['file_uploaded'] = True
            st.session_state['uploaded_data'] = pd.read_excel(uploaded_file)
            st.success("Excel file uploaded successfully!")
            emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
            if emails:
                st.session_state['emails'] = emails  # Store emails in session state
                st.write("Extracted Emails:")
                st.write(emails)
            else:
                st.error("No emails found in the 'user_email' column.")
            st.dataframe(st.session_state['uploaded_data'])

        if st.button("Generate Email Template"):
            st.session_state.email_template = email_generator(prompt, name, event_type, tone)
            st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)
        else:
            st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)

        uploaded_file = st.file_uploader("Choose a file to attach")

        if uploaded_file is not None:
            st.session_state.attachment = uploaded_file
            st.session_state.attachment_name = uploaded_file.name

        if st.session_state.attachment:
            st.write(f"Attached file: {st.session_state.attachment_name}")

        if st.button("Confirm and Send Emails"):
            st.write("Sending emails...")

            try:
                send_emails(emails, st.session_state.email_template, st.session_state.attachment, st.session_state.attachment_name)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3153.835434510016!2d144.96305781514882!3d-37.814107979751994!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ad642af0f11fd81%3A0xf57767ec3f59ffef!2sFederation%20Square!5e0!3m2!1sen!2sau!4v1627557207297!5m2!1sen!2sau" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', unsafe_allow_html=True)

    # Button to reset the session state and go back to the home page
    if page != "Home":
        if st.button("Go Back"):
            st.session_state['page'] = 'Home'
            st.session_state['event_type'] = None
            st.session_state['file_uploaded'] = False
            st.experimental_rerun()
               

if __name__ == "__main__":
    main()
