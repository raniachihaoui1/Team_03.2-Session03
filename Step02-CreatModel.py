"""Step 02: Create a Model in Speckle
====================================="""
## This script demonstrates how to create a new MODEL in Speckle





from main import get_client
from specklepy.core.api.inputs.model_inputs import CreateModelInput


## Your project ID
PROJECT_ID = "128262a20c" ##the homework folder created by Libny (for more info about creating project see Step01-CreateProject.py)
MODEL_NAME = "homework/session03/team_03.2_rc" ##name of the model to be created ## ID you ll need 61d71409ca

def main():
    client = get_client()

    # Create the model inside the project
    model = client.model.create(CreateModelInput(
        projectId=PROJECT_ID,
        name=MODEL_NAME,
        description="Model created for CW Session 03 by Team 03.2"
    ))


    print(f"✓ Created model: {model.id}")
    print(f"  Model name: {model.name}")
    print(f"  Project ID: {PROJECT_ID}")




if __name__ == "__main__":
    main()

