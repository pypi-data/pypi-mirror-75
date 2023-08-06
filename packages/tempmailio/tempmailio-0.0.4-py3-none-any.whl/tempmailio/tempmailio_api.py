# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Tuple, Optional

# Pip
from kcu import request

# Local
from .models.domain import Domain
from .models.email_address import EmailAddress
from .models.email import Email

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: TempMailIOAPI --------------------------------------------------------- #

class TempMailIOAPI:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @staticmethod
    def create_email(
        name: Optional[str],
        domain_name: Optional[str],
        fake_useragent: bool
    ) -> Optional[EmailAddress]:
        try:
            json_data = {}

            if name:
                json_data['name'] = name

            if domain_name:
                json_data['domain'] = domain_name

            return EmailAddress.from_dict(
                request.post(
                    'https://api.internal.temp-mail.io/api/v3/email/new',
                    data=json_data,
                    fake_useragent=fake_useragent
                ).json()
            )
        except Exception as e:
            print(e)

            return None

    @staticmethod
    def get_inbox(
        email_address: str,
        fake_useragent: bool = False
    ) -> Optional[List[Email]]:
        try:
            email_dicts = request.get(
                'https://api.internal.temp-mail.io/api/v3/email/{}/messages'.format(email_address),
                fake_useragent=fake_useragent
            ).json()
            emails = []

            for email_dict in email_dicts:
                try:
                    emails.append(Email.from_dict(email_dict))
                except Exception as e:
                    print(email_dict)
                    print(e)

                    pass

            return emails
        except Exception as e:
            print(e)

            return None

    @staticmethod
    def get_domains(
        fake_useragent: bool = False
    ) -> Optional[List[Domain]]:
        try:
            domain_dicts = request.get('https://api.internal.temp-mail.io/api/v3/domains', fake_useragent=fake_useragent).json()
            domains = []

            for domain_dict in domain_dicts:
                try:
                    domains.append(Domain.from_dict(domain_dict))
                except Exception as e:
                    print(domain_dict)
                    print(e)

                    pass

            return domains
        except Exception as e:
            print(e)

            return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #