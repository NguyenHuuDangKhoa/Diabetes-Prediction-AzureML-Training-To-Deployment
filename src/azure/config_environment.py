from azureml.core import Environment
from azureml.core import Workspace

def get_environment(ws: Workspace, name: str) -> Environment:
    """
    Get an registered environment from AzureML Studio
    :param ws: the current AzureML workspace
    :param name: name of an environment
    :return: an environment
    """
    env = Environment.get(workspace=ws, name=name)
    return env

def register_environment(ws: Workspace, name: str) -> Environment:
    """
    Register a new environment to AzureML Studio
    :param ws: the current AzureML workspace
    :param name: name of an environment to register
    :return: an environment
    """
    env = Environment.from_pip_requirements(name=name, file_path="./model_requirements.txt")
    env.register(workspace=ws)
    return env