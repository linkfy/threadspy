from client import *
from dotenv import load_dotenv
load_dotenv()


async def main():
    async with Client() as client:
        await client.generate_session_data(os.environ["USER"],os.environ["PASSWORD"])

asyncio.run(main())