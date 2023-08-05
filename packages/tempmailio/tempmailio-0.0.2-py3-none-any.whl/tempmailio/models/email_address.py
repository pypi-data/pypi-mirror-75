# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from jsoncodable import JSONCodable

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: EmailAddress ---------------------------------------------------------- #

class EmailAddress(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        address: str,
        token: str
    ):
        self.address = address
        self.token = token

        email_address_comps = address.split('@')

        self.user_name = email_address_comps[0]
        self.domain_name = email_address_comps[1]


    # --------------------------------------------------------- Static Init ---------------------------------------------------------- #

    @classmethod
    def from_dict(cls, json_dict: dict) -> Optional:
        try:
            return cls(
                address=json_dict['email'],
                token=json_dict['token']
            )
        except Exception as e:
            print(json_dict)
            print(e)

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #