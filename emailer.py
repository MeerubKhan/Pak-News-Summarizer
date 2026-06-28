import requests
import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

#load credntial
load_dotenv()
def send_digest(articles_with_summaries):
    sender=os.getenv('GMAIL_USER')
    receiver="hamidsaeed@gmail.com"
    password=os.getenv('GMAIL_PASSWORD')

#create email message structure
    msg=EmailMessage()
    msg['From']=sender
    msg['To']=receiver
    msg['Subject']='🇵🇰 Pakistani News Digest'

#body of email
    email_body=(
    f"Assalam Alikum here is your today's Pakistani News Digest\n\n"
    f"{'=' * 50 }\n\n"
    )
    for i,article in enumerate(articles_with_summaries,1):
        email_body+=f"{i}.{article['title']}\n"
        email_body+=f"Summary: {article['summary']}\n"
        email_body+=f"Read More at: {article['url']}\n"
        email_body+=f"{'-' * 50}\n\n"
    email_body+="\nThis digest was generated automatically by Pakistani News Summarizer :] "
    msg.set_content(email_body)

#creating secure connection
    print('connecting to Gmail Server... <3')
    context=ssl.create_default_context()

#send the email
    try:
       #using google secure port 465
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
            server.login(sender,password)
            print('Login Sucessful...Sending mail :)')
            server.send_message(msg)
            print("🎉 Success! Email sent successfully.")


    except Exception as e:
        print(f"\n❌ Error encountered: {e}")
