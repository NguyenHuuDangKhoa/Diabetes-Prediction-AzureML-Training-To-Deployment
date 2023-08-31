from azureml.core.model import Model
from pathlib import Path
from azureml.core import Workspace


def register_model(ws: Workspace, model_name: str, model_file: str) -> Model:
    """
    Register a model to AzureML Studio
    :param ws: AzureML workspace
    :param model_name: a path to a model which contains its name
    :return: a registered AzureML model 
    """
    model = Model.register(ws, model_name=model_name, model_path=model_file)
    return model