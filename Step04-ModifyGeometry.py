import copy
from main import get_client
from specklepy.api.operations import receive, send
from specklepy.transports.server import ServerTransport
from specklepy.core.api.inputs.version_inputs import CreateVersionInput
from specklepy.objects.base import Base

# --- CONFIG ---
PROJECT_ID = "128262a20c"
DEST_MODEL_ID = "61d71409ca"
TARGET_APP_ID = "17cc627f-f5df-44d2-908e-1cdaf96fe76c"
OFFSET_Z = 16000.0 

def find_object_deep(obj, target_id):
    if getattr(obj, "applicationId", None) == target_id: return obj
    names = obj.get_member_names() if hasattr(obj, "get_member_names") else []
    for name in names:
        prop = getattr(obj, name)
        if isinstance(prop, list):
            for item in prop:
                if isinstance(item, Base):
                    found = find_object_deep(item, target_id)
                    if found: return found
        elif isinstance(prop, Base):
            found = find_object_deep(prop, target_id)
            if found: return found
    return None

def offset_geometry(obj, offset_z):
    display_value = getattr(obj, "displayValue", None) or getattr(obj, "@displayValue", None)
    if display_value:
        meshes = display_value if isinstance(display_value, list) else [display_value]
        for mesh in meshes:
            if hasattr(mesh, "vertices"):
                v = list(mesh.vertices)
                for i in range(2, len(v), 3): v[i] += offset_z
                mesh.vertices = v
    for attr in ["basePoint", "location"]:
        pt = getattr(obj, attr, None)
        if pt and hasattr(pt, "z"): pt.z += offset_z

def main():
    client = get_client()
    transport = ServerTransport(client=client, stream_id=PROJECT_ID)

    # 1. Receive the existing data (modules collection)
    versions = client.version.get_versions(DEST_MODEL_ID, PROJECT_ID, limit=1)
    if not versions.items:
        print("Run Script 1 first.")
        return
    root_data = receive(versions.items[0].referenced_object, transport)

    # 2. Find and copy the Brep
    target_obj = find_object_deep(root_data, TARGET_APP_ID)
    new_geometry = copy.deepcopy(target_obj)
    new_geometry.applicationId = f"moved_{TARGET_APP_ID}_{OFFSET_Z}"
    
    # Set the Property "Module: 02"
    new_geometry["Module"] = "02"
    offset_geometry(new_geometry, OFFSET_Z)

    # 3. Create the "new modules" Base
    new_modules_base = Base()
    new_modules_base.name = "new modules"
    new_modules_base["@elements"] = [new_geometry]

    # 4. Add to the root elements so it sits NEXT TO 'old modules'
    if hasattr(root_data, "@elements"):
        # We append to the list so we don't lose the 'old modules' layer
        root_data["@elements"].append(new_modules_base)
    else:
        root_data["@elements"] = [new_modules_base]

    # 5. Send
    obj_id = send(root_data, [transport])
    client.version.create(CreateVersionInput(
        projectId=PROJECT_ID, modelId=DEST_MODEL_ID, objectId=obj_id,
        message="Added 'new modules' base with property 02"
    ))
    print("✓ Script 2 finished: 'new modules' is now side-by-side with 'old modules'.")

if __name__ == "__main__":
    main()