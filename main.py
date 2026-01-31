import os
from dotenv import load_dotenv
from specklepy.api.client import SpeckleClient



def get_client() -> SpeckleClient:
    load_dotenv()

    token = os.environ.get("SPECKLE_TOKEN")
    server_host = os.environ.get("SPECKLE_SERVER", "app.speckle.systems")

    if not token:
        raise ValueError("Set SPECKLE_TOKEN in your .env file and re-run.")

    # Authenticate
    client = SpeckleClient(host=server_host)
    client.authenticate_with_token(token)


    return client


if __name__ == "__main__":
    # Test authentication when running this script directly
    client = get_client()
    user = client.active_user.get()
    print(f"✓ Logged in as {user.name} on {client.url}")
