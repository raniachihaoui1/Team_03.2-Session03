"""Step 03: Copy Libny Model in New Model
====================================="""
## This script demonstrates how to copy objects from an existing Speckle model





from main import get_client
from specklepy.api.operations import receive, send
from specklepy.transports.server import ServerTransport
from specklepy.core.api.inputs.version_inputs import CreateVersionInput
from specklepy.objects.base import Base

PROJECT_ID = "128262a20c"
SOURCE_MODEL_ID = "a1014e4b32"
DEST_MODEL_ID = "61d71409ca"

def main():
    client = get_client()
    transport = ServerTransport(client=client, stream_id=PROJECT_ID)

    # 1. Receive data exactly as it is from the source
    versions = client.version.get_versions(SOURCE_MODEL_ID, PROJECT_ID, limit=1)
    source_root = receive(versions.items[0].referenced_object, transport)

    # 2. Create the main root (Collection)
    root_collection = Base()
    root_collection.speckle_type = "Speckle.Core.Models.Collection"
    root_collection.name = "modules"
    
    # 3. Create the layer (Layer)
    old_layer = Base()
    old_layer.speckle_type = "Objects.Organization.Layer"
    old_layer.name = "old modules"
    
    # 4. Pull the geometry directly from source elements to avoid nesting
    source_elements = getattr(source_root, "@elements", []) or getattr(source_root, "elements", [])
    old_layer["@elements"] = source_elements

    # 5. Place the layer inside the collection
    root_collection["@elements"] = [old_layer]

    # 6. Send
    obj_id = send(root_collection, [transport])
    client.version.create(CreateVersionInput(
        projectId=PROJECT_ID, 
        modelId=DEST_MODEL_ID, 
        objectId=obj_id, 
        message="Transferred old modules into new structure"
    ))
    print("✓ Script 1: Only old modules transferred.")

if __name__ == "__main__":
    main()