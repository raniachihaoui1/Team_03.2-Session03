import os
from dotenv import load_dotenv
from specklepy.api.client import SpeckleClient

# 1. This reads your .env file
load_dotenv()
token = os.getenv("SPECKLE_TOKEN")

# 2. This sets up the connection
client = SpeckleClient(host="https://app.speckle.systems")

# 3. This is the "Identity Check"
client.authenticate_with_token(token)

# 4. Verify it's really you
me = client.active_user.get()
print(f"I am now logged in as: {me.name} (ID: {me.id})")