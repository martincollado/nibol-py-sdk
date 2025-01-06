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

nibol = NibolClient(base_url="https://api.nibol.com/public", api_key="your_api_key")
bookings = nibol.bookings.get_bookings(query)
print(bookings)
```

### Async Client

```python
from nibol import NibolAsyncClient

async def main():
    nibol = NibolAsyncClient(base_url="https://api.nibol.com/public", api_key="your_api_key")
    bookings = await nibol.bookings.get_bookings(query)
    print(bookings)
```
