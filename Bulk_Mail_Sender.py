import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
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

        self.smtp_connection.ehlo()
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.sender_email, self.sender_password)

        self.file_attachment_path = 'Mail_Templates_and_Attachments/Tennant_CV.pdf'
    
    def generating_all_emails(self,list_of_listings):
        message = """
            <html>
            <body>
                <p>Dear {agent_name} of {agency},</p>
                <p>I hope this email finds you well. I am writing to express my strong interest in the {bed_rooms} bedroom {type} listing for {address_str}, which I came across on realestate.com.au.</p>
                <p>After reviewing the property details and photos, I believe that this property could be an excellent fit for my needs. In light of this, I would like to formally ask if the listing is still available, and if so request an inspection of the property.</p>
                <p>I would like to arrange a time and date that is convenient for both of us, so that I can view the property in person and get a better sense of its potential. </p>
                <p>I am very serious about my interest and would like to move forward with an inspection as soon as possible.</p>
                <p>My phone number is 0421 394037 and I am happy to share any additional documents relating to the claims mentioned in my CV as well.</p>
                <p>Thank you for your time and consideration, and I look forward to hearing from you soon.</p>
                <br>
                <p>Best regards,</p>
                <p>Kilian Voss</p>
            </body>
            </html>
        """
        # And if you're interested i can provide you the necessary documents relating to my financials (payslips,proof of ballance) and employment (contract).

        # html_message = """
        #     <html>
        #     <body>
        #         <p>Dear {agent_name} of {agency},</p>
        #         <p>I hope this email finds you well. I am writing to express my strong interest in the {bed_rooms} bedroom {type} listing for {address_str} which I came across on realestate.com.au.</p>
        #         <p>After reviewing the property details and photos, I believe that this property could be an excellent fit for my needs. In light of this, I would like to formally ask if the listing is still available and if so request an inspection of the property.</p>
        #         <p>I would like to arrange a time and date that is convenient for both of us so that I can view the property in person and get a better sense of its potential. I am very serious about my interest and would like to move forward with an inspection as soon as possible.</p>
        #         <p>My phone number is {phone} and I am happy to share any additional documents mentioned in my CV as well.</p>
        #         <p>Thank you for your time and consideration, and I look forward to hearing from you soon.</p>
        #         <p>Best regards,</p>
        #         <p>{first_name} {last_name}</p>
        #     </body>
        #     </html>"""

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

    def send_all_emails(self,essential_info_dicts):
        for listing in essential_info_dicts:
            # Set up the message parameters
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = listing['agent_mail']
            msg['Subject'] = listing['mail_subject']
            msg.attach(MIMEText(listing['mail_text'], 'html'))

            # Attach the file to the email
            with open(self.file_attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype=os.path.splitext(self.file_attachment_path)[1][1:])
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.file_attachment_path))
                msg.attach(attachment)

            # Send the message
            self.smtp_connection.sendmail(self.sender_email, listing['agent_mail'], msg.as_string())
        
        self.smtp_connection.quit()
        