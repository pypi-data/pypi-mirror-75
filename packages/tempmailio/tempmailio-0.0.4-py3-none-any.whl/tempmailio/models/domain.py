# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Domain ------------------------------------------------------------- #

class Domain(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        name: str,
        type: str,
        forward_available: bool
    ):
        self.name = name
        self.type = type
        self.pulic = type.lower() == 'public'
        self.forward_available = forward_available


    # --------------------------------------------------------- Static Init ---------------------------------------------------------- #

    @classmethod
    def from_dict(
        cls,
        json_dict: dict
    ) -> Optional:
        try:
            return cls(
                name=json_dict['name'],
                type=json_dict['type'],
                forward_available=json_dict['forward_available']
            )
        except Exception as e:
            print(json_dict)
            print(e)

            return None


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    # @property
    @classmethod
    def inboxme(cls):
        return cls('inbox-me.top', 'public', False)

    # @property
    @classmethod
    def inscriptio(cls):
        return cls('inscriptio.in', 'public', False)

    # @property
    @classmethod
    def cloudmail(cls):
        return cls('cloud-mail.top', 'public', False)

    # @property
    @classmethod
    def montokop(cls):
        return cls('montokop.pw', 'public', True)

    # @property
    @classmethod
    def privacymail(cls):
        return cls('privacy-mail.top', 'public', False)

    # @property
    @classmethod
    def safemail(cls):
        return cls('safemail.icu', 'public', False)

    # @property
    @classmethod
    def myinbox(cls):
        return cls('myinbox.icu', 'public', True)

    # @property
    @classmethod
    def random(cls):
        import random

        return random.choice(
            [
                cls.inboxme(),
                cls.inscriptio(),
                cls.cloudmail(),
                cls.montokop(),
                cls.privacymail(),
                cls.safemail(),
                cls.myinbox()
            ]
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #