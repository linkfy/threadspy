# Threadspy - Unofficial Threads Meta Api

## Installation
Clone the project, execute this instruction inside main folder to install packages:

```shell
pip install -r requirements.txt
```

## API
At the moment the API is experimental:
- client.login(user, passsword)
- client.post_message("Message from threads.net") (Links accepted)
- client.post_message("message", "https://www.threads.net/") (Link attachment accepted)

## Example usage

```python
from client import *
from dotenv import load_dotenv
load_dotenv()


async def main():
    async with Client() as client:
        token = await client.login(os.environ["USER"],os.environ["PASSWORD"])
        result = await client.post_message("Test client api")

asyncio.run(main())
```