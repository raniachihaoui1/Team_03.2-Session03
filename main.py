import os
from dotenv import load_dotenv
from specklepy.api.client import SpeckleClient

load_dotenv()
token = os.getenv("SPECKLE_TOKEN")

client = SpeckleClient(host="https://app.speckle.systems")
client.authenticate_with_token(token)

# This is the correct way for the new SDK:
user = client.active_user.get()
print(f"Successfully authenticated: {user.name}")