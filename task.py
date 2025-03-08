"""
    Task file.
"""

import os
import requests
import smtplib
from smtplib import SMTPResponseException
from dotenv import load_dotenv



def send_email(**kwargs):
    """Function to send an email with SMTP"""
    load_dotenv()
    my_email = os.environ.get("MY_EMAIL")
    app_password = os.environ.get("APP_PASSWORD")
    email = kwargs["email"]
    body = kwargs["body"]
    subject = kwargs["subject"]
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        try:
            connection.login(
                user= my_email,
                password=app_password
                )
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email,
                msg=f"Subject: {subject}!\n\n{body}")
        except SMTPResponseException as e:
            print(e)

def send_user_registration_email(email, username):
    """Function to send an email."""

    send_email(
        name=username,
        email= email,
        subject=f"{username}, you've successfully signed up!",
        body=f"Congratulations {username}, you just register with us! You are truly awesome!"
    )
