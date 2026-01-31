"""Step 01: Create a Project in Speckle
====================================="""
## This script demonstrates how to create a new PROJECT in Speckle


## Projects must belong to a workspace. You can find your workspace ID in the Speckle web interface 
# URL:# https://app.speckle.systems/settings/workspaces/macad-iaac/general

from main import get_client
from specklepy.core.api.inputs.project_inputs import WorkspaceProjectCreateInput
from specklepy.core.api.enums import ProjectVisibility

# Your workspace ID
WORKSPACE_ID = "a1cd06bae2"


def main():
    client = get_client()

    # Create the project
    project = client.project.create_in_workspace(WorkspaceProjectCreateInput(
        name="CW26-Sessions/homework/session03/team_03.2",
        description="Project created for CW Session 03 by Team 03.2",
        visibility=ProjectVisibility.PRIVATE,
        workspaceId=WORKSPACE_ID
    ))

    print(f"✓ Created project: {project.id}")

    # Verify project details
    project_details = client.project.get(project.id)
    print(f"  Project name: {project_details.name}")
    print(f"  Visibility:   {project_details.visibility}")

if __name__ == "__main__":
    main()