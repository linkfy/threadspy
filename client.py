import os
import json
import random
import aiohttp
import asyncio
from base64 import b64decode
from dotenv import load_dotenv
from endpoints import *
from utils import *


class Client:
    async def __aenter__(self):
        self.session = await self.new_session()
        self.device_id = None
        self.token = None
        self.user_id = None
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def new_session(self):
        return aiohttp.ClientSession(trust_env=True)

    async def login(self, username, password):
        headers = HEADERS_DEFAULT.copy()
        body = f'params={{"client_input_params":{{"password":"{password}","contact_point":"{username}","device_id":"{self.device_id}"}}, "server_params":{{"credential_type":"password","device_id":"{self.device_id}"}}}}&bk_client_context={{"bloks_version":"5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73","styles_id":"instagram"}}&bloks_versioning_id=5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73'
        async with self.session.post(LOGIN_URL, headers=headers, data=body) as res:
            text = await res.text()
            pos = text.find("Bearer IGT:2:")
            token = text[pos+13:pos+173]
            self.token = token
            self.user_id = json.loads(b64decode(token).decode('utf8'))['ds_user_id']
            self.device_id = "android-"+ format(random.randint(0, int(1e24)), '36')
            return token
    
    async def post_message(self, message):
        url = API_URL + "media/configure_text_only_post/"
        headers = HEADERS_DEFAULT.copy()

        headers.update({'Authorization': 'Bearer IGT:2:' + self.token})
        body_data = {
            "publish_mode": "text_post",
            "text_post_app_info": "{\"reply_control\":0}",
            "timezone_offset": "7200",
            "source_type": "4",
            "_uid": self.user_id,
            "device_id": self.device_id,
            "caption": message,
            "upload_id": random.randint(10**13, 10**14 - 1),
            "device": {
                "manufacturer": "samsung",
                "model": "SM-N976N",
                "android_version": 25,
                "android_release": "7.1.2"
            }
        }
        body = {
            "signed_body":f"SIGNATURE.{json.dumps(body_data)}"
        }

        
        async with self.session.post(POST_URL, headers=headers , data=body) as res:
            post_result = await res.json()
            return post_result
        

    async def get_lsd():
        async with self.session.get("https://www.threads.net/@linkfytester") as res:
            text = await res.text()
            pos = text.find("\"token\"")
            lsd = text[pos + 9: pos + 31]
            return lsd