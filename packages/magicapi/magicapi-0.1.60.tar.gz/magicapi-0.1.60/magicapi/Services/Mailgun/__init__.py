from typing import List
import requests

# from magicapi import settings
from magicapi import g


def send_email(text: str, recipients: List[str], subject: str = ""):
    return requests.post(
        f"https://api.mailgun.net/v3/{g.settings.mailgun_domain_name}/messages",
        auth=("api", g.settings.mailgun_private_api_key),
        data={
            "from": f"{g.settings.mailgun_sender_name} <{g.settings.mailgun_sender_email}>",
            "to": recipients,
            "subject": subject,
            "text": text,
        },
    )


if __name__ == "__main__":
    resp = send_email(
        recipients=["kellycup8@aim.com"], text="jey man", subject="yessir"
    )
    print("resp content", resp.content)
