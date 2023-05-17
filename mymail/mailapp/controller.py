import imaplib
import email
import smtplib
from django.conf import settings

def receive_mail_content(user_email, user_password):
    try:
        with imaplib.IMAP4_SSL(settings.IMAP_SERVER) as mail:
            mail.login(user_email, user_password)
            mail.select('inbox')

            _, data = mail.search(None, 'ALL')
            # Retrieve the latest 10 message ids
            email_ids = data[0].split()[-10:]

            emails = []
            for email_id in email_ids:
                _, msg_data = mail.fetch(email_id, '(RFC822)')
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                body = None
                # get Body
                if email_message.is_multipart():
                    # If the email has multiple parts, iterate over them
                    for part in email_message.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload()
                            break
                else:
                    # If the email has a single part, directly retrieve the body
                    body = email_message.get_payload()

                # Parse the headers of the email message
                emails.append({'From': email_message['From'], 
                                'To': email_message['To'], 
                                'Subject': email_message['Subject'], 
                                'Date': email.utils.parsedate_to_datetime(email_message['Date']), 
                                'Body': body,
                                })
                
            return emails
    except imaplib.IMAP4.error as err:
        raise err
    

def send_email_content(recipient, subject, message, user_email, user_password):
    try:
        msg = email.message.EmailMessage()

        msg['From'] = user_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Set the body of the email
        msg.set_content(message)
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(user_email, user_password)

            server.send_message(msg)

    except smtplib.SMTPException as err:
        raise err