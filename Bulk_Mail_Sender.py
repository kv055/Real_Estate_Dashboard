import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

class EmailSender:
    
    def __init__(self):
        
        # Access the environment variables
        self.smtp_server = os.getenv('smtp_server')
        self.smtp_port = os.getenv('smtp_port')
        self.sender_email = os.getenv('sender_username')
        self.sender_password = os.getenv('sender_password')
        # Set up the SMTP server
        self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.smtp_connection.connect()
        self.smtp_connection.ehlo()
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.sender_email, self.sender_password)
    
    def generating_all_emails(self,list_of_listings):
        message = '''Dear {agent_name} of {agency},
        I hope this email finds you well. I am writing to express my strong interest in the
        {bed_rooms} bedroom {type} listing for {address_str}, which I came across on realestate.com.au.
        After reviewing the property details and photos, I believe that this property could be an excellent fit for my needs.
        In light of this, I would like to formally ask if the listing is still available,
        and if so request an inspection of the property.
        I would like to arrange a time and date that is convenient for both of us,
        so that I can view the property in person and get a better sense of its potential.
        I am very serious about my interest and would like to move forward with an inspection as soon as possible.
        My phonenumber is 0421 394037 and i am happy to share any additional documents metioned in my CV as well.
        Thank you for your time and consideration, and I look forward to hearing from you soon.

        Best regards,

        Kilian Voss'''
        for listing in list_of_listings:
            formatted_message = message.format(
                agent_name=listing['agent_name'], 
                agency=listing['agency'], 
                bed_rooms=listing['bed_rooms'], 
                type=listing['type'], 
                address_str=listing['address_str'])
            
            formatted_message = formatted_message.replace('\n', '')
        
            listing['mail_text'] = formatted_message
            listing['mail_subject'] = f"""Request for Inspection {listing['address_str']}"""

    def preparing_all_emails(self,essential_info_dicts):
        for listing in essential_info_dicts:
            # Set up the message parameters
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(listing['agent_mail'])
            msg['Subject'] = listing['mail_subject']
            msg.attach(MIMEText(listing['mail_text'], 'plain'))
        
    # def send_all_emails(self):
    #     # Send the message
    #     self.smtp_connection.sendmail(self.sender_email, recipient_emails, msg.as_string())
        
    #     # Close the SMTP connection
    #     self.smtp_connection.quit()
