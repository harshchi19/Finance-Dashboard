from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv
import os
import asyncio
import streamlit as st
from infomatrix import infomatrix

load_dotenv('.env')

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URL')
client = GoogleOAuth2(client_id, client_secret)

async def get_authorization_url(client, redirect_uri):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["openid", "profile", "email"])
    return authorization_url

async def get_access_token(client, redirect_uri, code):
    token = await client.get_access_token(code, redirect_uri)
    return token

def get_login_str():
    authorization_url = asyncio.run(get_authorization_url(client, redirect_uri))
    return f'''<a target="_self" href="{authorization_url}">Google Login</a>'''

def authenticate_user():
    query_params = st.experimental_get_query_params()

    if 'code' in query_params:
        code = query_params['code'][0]
        token = asyncio.run(get_access_token(client, redirect_uri, code))
        
        st.experimental_set_query_params(page="infomatrix")
        if st.experimental_get_query_params().get("page") == ["infomatrix"]:
            infomatrix()  
            return

authenticate_user()
