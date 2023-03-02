import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the SMTP server
smtp_server = 'smtp.live.com'
# smtp-mail.outlook.com
# smtp.live.com
# smtp.office365.com
smtp_port = 587
smtp_username = 'kilian96@live.de'
smtp_password = 'your_email_password'
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.ehlo()
smtp_connection.starttls()
smtp_connection.login(smtp_username, smtp_password)

# Set up the message parameters
sender_email = 'kilian96@live.de'
recipient_emails = ['kilivoss@gmail.com', 'kilivo.kv@gmail.com']
message_subject = 'Test email'
message_body = 'Hello world!'
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ', '.join(recipient_emails)
msg['Subject'] = message_subject
msg.attach(MIMEText(message_body, 'plain'))

# Send the message
smtp_connection.sendmail(sender_email, recipient_emails, msg.as_string())

# Close the SMTP connection
smtp_connection.quit()
