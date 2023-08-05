# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import datetime

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Email ------------------------------------------------------------- #

class Email(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self
    ):
        pass


    # --------------------------------------------------------- Static Init ---------------------------------------------------------- #

    @classmethod
    def from_dict(cls, json_dict: dict) -> Optional:
        try:
            email = Email()

            email.id = json_dict['id']
            email.sender = json_dict['from']
            email.sender_address = email.sender.split('<')[-1].replace('>', '').strip()
            email.to = json_dict['to']
            email.cc = json_dict['cc']
            email.subject = json_dict['subject']
            email.body_text = json_dict['body_text']
            email.body_html = json_dict['body_html']
            email.created_at_str = json_dict['created_at']
            email.created_at_timestamp = datetime.datetime.strptime(email.created_at_str[:26], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
            email.attachments = json_dict['attachments']

            return email
        except Exception as e:
            print(json_dict)
            print(e)

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #