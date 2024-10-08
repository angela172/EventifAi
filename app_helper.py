import streamlit as st
from langchain_community.llms import Ollama
import pandas as pd
import json

# Initialize the LLM
llm = Ollama(model="llama3:latest")

def extract_emails(df, column_name):
    if column_name in df.columns:
        emails = df[column_name].dropna().unique().tolist()
        return emails
    else:
        return []

# Function to display the chatbot for collecting event details
'''def event_chatbot(emails):
    prompt = st.text_area("Enter the event details:")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                refined_prompt = f"""Generate event details for Google Calendar in the following JSON format. Only give the JSON format and don't type 
                 any other text:
                       {{
                            'summary': 'Meeting with John',
                            'location': '123 Main St, Anytown, USA',
                            'description': 'Discuss project updates',
                            'start_time': '2024-07-01T10:00:00-07:00',
                            'end_time': '2024-07-01T11:00:00-07:00',
                            'time_zone': 'America/Los_Angeles',
                            'attendees': {emails}
                        }}
                  Event = "{prompt}"
                """
            #st.write_stream(llm.stream(refined_prompt, stop=['<|eot_id|>']))
            response = llm.invoke(refined_prompt, stop=['<|eot_id|>'])
            st.write(response)

            # Write the prompt to a file
            with open("prompt.txt", "w") as f:
                f.write(response)'''


# Function to display the chatbot for collecting event details
def event_chatbot(emails, user_prompt):
    refined_prompt = f"""
    Generate event details for Google Calendar in the following JSON format. Only give the JSON format and don't type 
    any other text:
    {{
        "summary": 'Meeting with John',
        "location": '123 Main St, Anytown, USA',
        "description": 'Discuss project updates',
        "start_time": '2024-07-01T10:00:00-07:00',
        "end_time": '2024-07-01T11:00:00-07:00',
        "time_zone": 'America/Los_Angeles',
        "attendees": {emails}
    }}
    Event = "{user_prompt}"
    """
    # Dummy LLM invocation - replace with actual LLM call
    #response = "This is a dummy response from the AI model."
    response = llm.invoke(refined_prompt, stop=['<|eot_id|>'])
    #st.write(response)
    return response

def email_generator(prompt, name, event_type, tone):
    llm = Ollama(model="llama3")
    
    if tone.lower() == "formal":
        refined_prompt = f"""Create a formal email invitation for an event about {event_type} in the following format. Only give the email body and don't type any other text beofre and after it:
        
        Dear all,
        I would like to invite you to the {event_type} event on [Date].
        
        RSVP
        Best regards,
        {name}
        
        Event = "{prompt}"
        """
    if tone.lower() == "informal":
        refined_prompt = f"""Create an informal email invitation for an event about {event_type} in the following format. Only give the email body and don't type any other text before and after it:
        
        Hey guys,
        Join us for a [event_type] event on [Date] from [start_time] to [end_time]!
        
        RSVP y'all
        Cheers,
        {name}
        
        Event = "{prompt}"
        """
    response = llm.invoke(refined_prompt, stop=['<|eot_id|>'])
    return response