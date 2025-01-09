# [Non Oficial] Nibol Python SDK

**Non-official** Python SDK for the Nibol API. For more information go to Nibol support.


> [!WARNING]  
> It's experimental development for integrations purpose. Probably I'll finish error handling, docs, add comments and publish it on PyPi.


## Installation

```bash
pip install nibol
```

## Usage

```python
from nibol import NibolClient

nibol = NibolClient(base_url="https://api.nibol.com/public", api_key="your_api_key", api_email="you_email_api")
users = nibol.users.list_users(emails=["jon@example.com"])
print(bookings)
```