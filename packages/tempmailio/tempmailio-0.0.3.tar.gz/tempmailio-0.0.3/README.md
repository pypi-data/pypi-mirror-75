# tempmailio

![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/tempmailio?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/tempmailio)

## Description

python wrapper for tempmail.io

## Install

````bash
pip install tempmailio
# or
pip3 install tempmailio
````

## Usage

```python
import time

from tempmailio import *

mail = TempMailI0(
    user_name='test',
    domain=Domain.cloudmail()
)

success = mail.create_email()

print(mail.email_address)

while True:
    inbox = mail.get_inbox()

    if len(inbox) > 0mermaid :
        inbox[0].jsonprint()
        exit(0)

    time.sleep(2.5)
```
