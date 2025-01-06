# Nibol Python SDK

Python SDK for the Nibol API.

## Installation

```bash
pip install nibol
```

## Usage

### Sync Client

```python
from nibol import NibolClient

nibol = NibolClient(base_url="https://api.nibol.com/public", api_key="your_api_key", api_email="you_email_api")
users = nibol.users.list_users(emails=["jon@example.com"])
print(bookings)
```