import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

# Mailer server
smtp_server = os.getenv("MAILER_SERVER")
# Mailer port
smtp_port = os.getenv("MAILER_PORT")
# Email ID of sender
smtp_username = os.getenv("EMAIL_ID")
# Email password of sender
smtp_password = os.getenv("EMAIL_PASSWORD")
# Recipient for email
recipient = os.getenv("RECIPIENT")

# Function to send contact form email to customer support
def send_contact_email(data):
    # DATA from user
    email = str(data.get('email'))
    name = str(data.get('name'))
    company = str(data.get('company_name'))
    message = str(data.get('message'))
    phone = str(data.get('phone'))
    # Mail specific data
    subject = f"Contact request from {name} of {company}"
    mail_body = f"Name: {name},\nCompany Name: {company},\nPhone No.: {phone},\nEmail: {email},\nMessage: {message}"
    # Establish connection to the SMTP server
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    # Login to the SMTP server
    server.login(smtp_username, smtp_password)    
    try:
        # Create a test email message
        msg = MIMEText(mail_body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = recipient
        # Send the test email
        server.sendmail(smtp_username, recipient, msg.as_string())
        return 'Mail sent succesfully'
    except Exception as e:
         # Capture specific error messages from smtplib exceptions
        error_message = str(e)
        print(f"Error sending email: {error_message}")
        return f'SMTP connection error: {error_message}', 500  # Internal Server Error
    finally:
        # Close the connection to the SMTP server
        if server:
            server.quit()
