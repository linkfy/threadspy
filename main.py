from client import *
from dotenv import load_dotenv
load_dotenv()


async def main():
    async with Client() as client:
        token = await client.login(os.environ["USER"],os.environ["PASSWORD"])
        result = await client.post_message("Test client api", "https://www.threads.net/")

asyncio.run(main())