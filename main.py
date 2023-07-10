from client import *


async def main():
    async with Client() as client:
        await client.login()
        result0 = await client.post_message(image="firefox.jpg")
        # This lines are commented so avoid Massive calls = Spam detection, remember to not do massive actions, add timers too (time.sleep(60), etc..)
        #result0_post_id = result0["media"]["pk"]
        #result0_1 = await client.like_post(result0_post_id)
        #result1 = await client.post_message("Uno", image="firefox.jpg")
        #result2 = await client.post_message("Dos", link_attachment="https://twitter.com")
        #result3 = await client.post_message("Tres", image="firefox.jpg", link_attachment="https://chrome.com")
        #print(result0, result0_1, result1, result2, result3)

asyncio.run(main())