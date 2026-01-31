from main import get_client
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.objects.base import Base
from specklepy.core.api.inputs.version_inputs import CreateVersionInput

# --- CONFIG ---
PROJECT_ID = "128262a20c"
MODEL_ID = "61d71409ca"

client = get_client()

# 1. Fetch data
latest_version = client.version.get_versions(MODEL_ID, PROJECT_ID, limit=1).items[0]
transport = ServerTransport(client=client, stream_id=PROJECT_ID)
data = operations.receive(latest_version.referenced_object, transport)

# 2. Simple Recursive Search and Update
def update_designers_by_module(obj):
    # Check if this object has a 'Module' property in its data or properties
    # We check both the root and the 'properties' dictionary
    module_val = None
    
    # Check root level
    if hasattr(obj, "Module"):
        module_val = obj["Module"]
    # Check inside properties dictionary
    elif "properties" in obj.get_member_names() and "Module" in obj["properties"]:
        module_val = obj["properties"]["Module"]

    # If we found a Module number, assign the Designer
    if module_val:
        if "properties" not in obj.get_member_names():
            obj["properties"] = {}
            
        if module_val == "01":
            obj["properties"]["Designer"] = "Eleni ✨"
        elif module_val == "03":
            obj["properties"]["Designer"] = "Eduardo ✨"
        else:
            # The "other left one" (Module 02)
            obj["properties"]["Designer"] = "Rania ✨"

    # Keep looking deeper through all elements
    elements = getattr(obj, "@elements", None) or getattr(obj, "elements", [])
    for el in elements or []:
        if isinstance(el, Base):
            update_designers_by_module(el)
    
    # Also check any other dynamic properties that might be Base objects
    for name in obj.get_member_names():
        if name.startswith("@") or name == "elements": continue
        prop = getattr(obj, name)
        if isinstance(prop, Base):
            update_designers_by_module(prop)

# Run the update
update_designers_by_module(data)
print("✓ Finished scanning all objects and updating Designers by Module number.")

# 3. Send and Create Version
object_id = operations.send(data, [transport])
version = client.version.create(
    CreateVersionInput(
        projectId=PROJECT_ID,
        modelId=MODEL_ID,
        objectId=object_id,
        message="Updated Designers: 01=Eleni ✨, 03=Eduardo ✨, others=Rania ✨",
    )
)

print(f"✓ Created new version: {version.id}")