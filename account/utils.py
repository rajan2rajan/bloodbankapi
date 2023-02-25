from django.core.mail import EmailMessage
import os
from django.conf import settings
from django.core.mail import send_mail

# this is to send the email to those who do login
def send(link,email):
    try:
        subject = 'your account need to be verify'
        message = f'Hi thank you for registering in geeksforgeeks. {link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email ]
        send_mail( subject, message, email_from, recipient_list )

        
    except Exception as e:
        return False
    
    return True


def approved(email):
    try:
        subject = 'blood recived accepted '
        message = f'your message has been accepted. we will contact you in short time  '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email ]
        send_mail( subject, message, email_from, recipient_list )
     
    except Exception as e:
        return False
    
    return True

def decline(email):
    try:
        subject = 'blood recived decline '
        message = f'your message has been declined '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email ]
        send_mail( subject, message, email_from, recipient_list )
     
    except Exception as e:
        return False
    
    return True