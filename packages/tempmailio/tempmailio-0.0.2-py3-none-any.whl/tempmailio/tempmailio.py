# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Tuple, Optional

# Pip
from kcu import request

# Local
from .tempmailio_api import TempMailIOAPI
from .models.domain import Domain
from .models.email_address import EmailAddress
from .models.email import Email

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: TempMailIo ----------------------------------------------------------- #

class TempMailI0:
    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        user_name: Optional[str],
        domain: Optional[Domain],
        fake_useragent: bool = False
    ):
        self.user_name = user_name
        self.domain = domain
        self.email_address = user_name + '@' + domain.name
        self.fake_useragent = fake_useragent

    def create_email(
        self,
        fake_useragent: Optional[bool] = None
    ) -> bool:
        new_address = TempMailIOAPI.create_email(
            name=self.user_name,
            domain_name=self.domain.name,
            fake_useragent=fake_useragent or self.fake_useragent
        )

        if new_address is None:
            return False

        self.user_name = new_address.user_name
        self.domain.name = new_address.domain_name
        self.email_address = new_address.address

        return True

    def get_inbox(
        self,
        fake_useragent: Optional[bool] = None
    ) -> Optional[List[Email]]:
        return TempMailIOAPI.get_inbox(
            email_address=self.email_address,
            fake_useragent=fake_useragent or self.fake_useragent
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #