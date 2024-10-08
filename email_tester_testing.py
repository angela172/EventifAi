import streamlit as st
from app_helper import *
import base64
import mimetypes
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar'
]

def send_email_with_attachment(to, subject, body, attachment_data, attachment_name, creds):
    # Create the email
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    # Attach the email body as plain text
    msg = MIMEText(body, 'plain')
    message.attach(msg)

    # Attach the file if any
    if attachment_data:
        content_type, encoding = mimetypes.guess_type(attachment_name)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        attachment_part = MIMEBase(main_type, sub_type)
        attachment_part.set_payload(attachment_data)
        encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        message.attach(attachment_part)

    # Encode the email in base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw_message}

    # Send the email
    service = build('gmail', 'v1', credentials=creds)
    try:
        service.users().messages().send(userId='me', body=body).execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def send_emails(recipients, email_body, attachment, attachment_name):
    # recipients = ["f20210183@dubai.bits-pilani.ac.in"]  # List of recipients
    subject = "Party Invitation"
    
    # Load your credentials
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Read attachment data if any
    attachment_data = attachment.read() if attachment else None

    for recipient in recipients:
        send_email_with_attachment(recipient, subject, email_body, attachment_data, attachment_name, creds)
    
    st.success("Emails sent successfully!")

# def main():
#     # Streamlit app
#     st.title("Email Template Generator")

#     if "email_template" not in st.session_state:
#         st.session_state.email_template = ""
#     if "attachment" not in st.session_state:
#         st.session_state.attachment = None
#     if "attachment_name" not in st.session_state:
#         st.session_state.attachment_name = None

#     event_type = st.text_input("Enter the type of event:")

#     tone = st.radio("Choose the tone of the email:", ("formal", "informal"))
#     name = st.text_input("Enter your name:")
#     prompt = st.text_input("Type your prompt here (don't forget to mention the date and time!): ")
    
#     if st.button("Generate Email Template"):
#         st.session_state.email_template = email_generator(prompt, name, event_type, tone)
#         st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)
#     else:
#         st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)    
    
#     uploaded_file = st.file_uploader("Choose a file to attach")
        
#     if uploaded_file is not None:
#         st.session_state.attachment = uploaded_file
#         st.session_state.attachment_name = uploaded_file.name

#     if st.session_state.attachment:
#         st.write(f"Attached file: {st.session_state.attachment_name}")

#     if st.button("Confirm and Send Emails"):
#         st.write("Sending emails...")
        
#         try:
#             send_emails(st.session_state.email_template, st.session_state.attachment, st.session_state.attachment_name)
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()
