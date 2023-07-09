# Threadspy - Unofficial Threads Meta Api

<p align="center">
  <img src=".github/cover.jpg" alt="cover" width="500px" />
</p>

## Installation
Clone the project, execute this instruction inside main folder to install packages:

```shell
pip install -r requirements.txt
```

## API
At the moment the API is experimental:
- client.login(user, passsword)
- client.post_message("Message from threads.net") (Links accepted)
- client.post_message("message", link_attachment="https://www.threads.net/") (Link attachment accepted)
- client.post_message("message",  image="firefox.jpg") (Image attachment accepted)
- client.post_message(image="firefox.jpg") (Upload only images)

Extra:
- Delete "session_data.json" to regenerate login sessions after first login

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

## More examples

```python
from client import *
from dotenv import load_dotenv
load_dotenv()


async def main():
    async with Client() as client:
        await client.login(os.environ["USER"],os.environ["PASSWORD"])
        result0 = await client.post_message(image="firefox.jpg")
        result1 = await client.post_message("One", image="firefox.jpg")
        result2 = await client.post_message("Two", link_attachment="https://twitter.com")
        result3 = await client.post_message("Three", image="firefox.jpg", link_attachment="https://chrome.com")
        print(result0, result1, result2, result3)


asyncio.run(main())
```