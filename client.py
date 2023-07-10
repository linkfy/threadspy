import os
import json
import random
import aiohttp
import aiofiles
import asyncio
from base64 import b64decode
from dotenv import load_dotenv
from endpoints import *
from utils import *
import uuid
import time

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

    async def generate_session_data(self, username, password):
        headers = HEADERS_DEFAULT.copy()
        body = f'params={{"client_input_params":{{"password":"{password}","contact_point":"{username}","device_id":"{self.device_id}"}}, "server_params":{{"credential_type":"password","device_id":"{self.device_id}"}}}}&bk_client_context={{"bloks_version":"5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73","styles_id":"instagram"}}&bloks_versioning_id=5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73'
        async with self.session.post(LOGIN_URL, headers=headers, data=body) as res:
            text = await res.text()
            pos = text.find("Bearer IGT:2:")
            token = text[pos+13:pos+173]
            self.token = token
            self.user_id = json.loads(b64decode(token).decode('utf8'))['ds_user_id']
            self.device_id = "android-"+ format(random.randint(0, int(1e24)), '36')

            session_data = {
                'user_id': f'{self.user_id}',
                'device_id': f'{self.device_id}',
                'token': f'{self.token}',
            }

            with open('session_data.json', 'w') as f:
                json.dump(session_data, f)

            return token
    
    async def login(self):
        try:
            with open('session_data.json', 'r') as f:
                session_data = json.load(f)
                self.user_id = session_data['user_id']
                self.token =  session_data['token']
                self.device_id =  session_data['device_id']
        except Exception as e:
            print(e)
    
    async def post_message(self, message="", link_attachment=None, image=None, post_id=None): 
        headers = HEADERS_DEFAULT.copy()
        headers.update({'Authorization': 'Bearer IGT:2:' + self.token})
        url = POST_URL

        body_data = {
            "publish_mode": "text_post",
            "text_post_app_info": {"reply_control": 0},
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
        
        if image:
            upload_id = json.loads(await self.upload_photo(image))['upload_id']
            body_data['upload_id'] = upload_id
            body_data.pop("publish_mode")
            url = POST_WITH_IMAGE_URL
        
        if post_id:
            body_data["text_post_app_info"].update({'reply_id': post_id})

        if link_attachment:
            body_data["text_post_app_info"].update({'link_attachment_url': link_attachment})

        body = {
            "signed_body":f"SIGNATURE.{json.dumps(body_data)}"
        }
        
        async with self.session.post(url, headers=headers , data=body) as res:
            post_result = await res.json()
            return post_result

    async def upload_photo(self, image_path):
        headers = HEADERS_DEFAULT.copy()
        headers.update({'Authorization': 'Bearer IGT:2:' + self.token})
        upload_id = int(time.time() * 1000)
        name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"
        filepath = f"{image_path}"
        url = "https://www.instagram.com/rupload_igphoto/" + name

        async with aiofiles.open(filepath, mode='rb') as f:
            content = await f.read()


        x_instagram_rupload_params = {
            "upload_id":f"{upload_id}",
            "media_type":"1",
            "sticker_burnin_params":"[]",
            "image_compression": json.dumps(
                {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
            ),
            "xsharing_user_ids":"[]",
            "retry_context":{
                "num_step_auto_retry":'0',
                "num_reupload":'0',
                "num_step_manual_retry":'0'
            },
            "IG-FB-Xpost-entry-point-v2":"feed"
        }
        contentLength = len(content)
        image_headers = {
            'X_FB_PHOTO_WATERFALL_ID': str(uuid.uuid4()),
            'X-Entity-Type': 'image/jpeg',
            'Offset': '0',
            'X-Instagram-Rupload-Params': json.dumps(x_instagram_rupload_params),
            'X-Entity-Name': f"{name}",
            'X-Entity-Length': f"{contentLength}",
            'Content-Type': 'application/octet-stream',
            'Content-Length': f"{contentLength}",
            'Accept-Encoding': 'gzip',
        }

        headers.update(image_headers)

        async with self.session.post(url, headers=headers, data=content) as response:
            return await response.text()

    async def update_media_with_pdq_hash_info(self, upload_id="87490918227685"):
        headers = HEADERS_DEFAULT.copy()

        headers.update({'Authorization': 'Bearer IGT:2:' + self.token})
        pdq_hash_info = {
                    "pdq_hash": "17b1b91bb94b46e417b1319346b4ce6ce84eec4e46b413b117b1b91bb94b46e4:89",
                    "frame_time": 0
        }

        body_data = {
            "pdq_hash_info": json.dumps(pdq_hash_info),
            "_uid": self.user_id,
            "_uuid": "3d8ce049-3663-4cfe-9417-08d152df3874",
            "upload_id": f"{upload_id}"
        }

        body = {
            "signed_body":f"SIGNATURE.{json.dumps(body_data)}"
        }
        
        async with self.session.post(UPDATE_MEDIA_PQD_HASH_URL, headers=headers , data=body) as res:
            post_result = await res.json()
            return post_result    

    async def get_lsd(self):
        async with self.session.get("https://www.threads.net/@linkfytester") as res:
            text = await res.text()
            pos = text.find("\"token\"")
            lsd = text[pos + 9: pos + 31]
            return lsd
        
    async def like_post(self, post_id=None, unlike=False):
        headers = HEADERS_DEFAULT.copy()

        headers.update({'Authorization': 'Bearer IGT:2:' + self.token})
        body_data = {
            "media_id": f"{post_id}",
            "_uid": self.user_id,
        }
        body = {
            "signed_body":f"SIGNATURE.{json.dumps(body_data)}"
        }

        action = "like" if unlike == False else "unlike"
        async with self.session.post(f"{API_URL}media/{post_id}/{action}/", headers=headers , data=body) as res:
            post_result = await res.json()
            return post_result

    async def get_post_id_from_url(self, url):
        async with self.session.get(url) as res:
            text = await res.text()
            pos = text.find("\"post_id\"")
            post_id = text[pos + 11: pos + 30]
            return post_id
