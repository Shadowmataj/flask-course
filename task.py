"""
    Task file.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_simple_message(to, subject, body):
    """Function to send an email."""
    mailgun_domain = os.environ.get("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY", "API_KEY")),
        data={
            "from": f"Mailgun Sandbox <postmaster@{mailgun_domain}>",
            "to": f"Custumer <{to}>",
            "subject": subject,
            "text": body,
        },
        timeout=10,
    )

def send_user_registration_email(email, username):
    """Function to send an email."""
    send_simple_message(
        to=email,
        subject="Successfully signed up!",
        body=f"Congratulations {username}, you just register with us! You are truly awesome!"
    )
