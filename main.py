# Custom Module
from src.azure.deployment import deploy_model

# Third-party Library

# Standard Library


"""
# For deployment, we need:
# 1/ Registered Model
# 2/ Software Environment
# 3/ Scoring Script
# 4/ Deployment Configuration
"""
def main():
    service = deploy_model()

if __name__ == "__main__":
    main()