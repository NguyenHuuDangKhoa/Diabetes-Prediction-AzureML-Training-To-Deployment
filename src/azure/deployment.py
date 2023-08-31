# Standard Library
import urllib.request

# Third-party Library
from azureml.core import Workspace
from pathlib import Path
from azureml.core.model import Model
from azureml.exceptions._azureml_exception import WebserviceException
from azureml.core import Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice

# Custom Module
from src.utils.load_yaml_config import load_yaml_config


def authenticate() -> Workspace:
    """
    Authenticate connection to AzureML Studio
    Using config.json file in .azureml at root directory
    """
    try:
        ws = Workspace.from_config()
        print(ws)
        return ws
    except:
        print('Workspace not found')


def download_pretrained_model(url: str, file_name: str, file_path: str) -> None:
    """
    Download a pretrained model to the models folder
    :param url: url of the model to be downloaded
    :param file: name to save the downloaded model
    :return: None
    """
    file_name = Path(file_path) / file_name
    if not file_name.exists():
        urllib.request.urlretrieve(url=url, filename=file_name)


def register_model(ws: Workspace, model_name: str, file_name: str, file_path: str) -> Model:
    """
    Register a model to AzureML Studio
    :param ws: AzureML workspace
    :param model_name: a path to a model which contains its name
    :return: a registered AzureML model 
    """
    file_path = Path(file_path) / file_name
    model = Model.register(ws, model_name=model_name, model_path=file_path)
    return model


def load_model(ws: Workspace, name: str) -> Model:
    model = Model(workspace=ws, name=name)
    return model


def get_environment(ws: Workspace, name: str) -> Environment:
    """
    Get an registered environment from AzureML Studio
    :param ws: the current AzureML workspace
    :param name: name of an environment
    :return: an environment
    """
    env = Environment.get(workspace=ws, name=name)
    return env

def register_environment(ws: Workspace, name: str, file_path: str) -> Environment:
    """
    Register a new environment to AzureML Studio
    :param ws: the current AzureML workspace
    :param name: name of an environment to register
    :return: an environment
    """
    env = Environment.from_pip_requirements(name=name, file_path=file_path)
    env.register(workspace=ws)
    return env


def config_scoring_script(env: Environment, entry_script: str, source_directory: str =".") -> InferenceConfig:
    """
    Configurate the scoring script
    :param env: an environment that would be used for deployment
    :param entry_script: the scoring script to evalute the model prediction
    :param source_directory: path to the scoring script
    :return: a configurated script for evaluating model prediction
    """
    inference_config = InferenceConfig(environment=env, source_directory=source_directory, entry_script=entry_script)
    return inference_config


def config_local_deployment(port: int) -> LocalWebservice:
    """
    Configurate the deployment of a model
    :param port: port for connect to the local host
    :return: a configurated local web service
    """
    deployment_config = LocalWebservice.deploy_configuration(port=port)
    return deployment_config


def config_cloud_deployment(cpu_cores: int, memory_gb: int, auth_enabled=True) -> AciWebservice:
    deployment_config = AciWebservice.deploy_configuration(cpu_cores=cpu_cores, memory_gb=memory_gb, auth_enabled=auth_enabled)
    return deployment_config


def deploy_model():
    # Connect to Azure ML Studio
    ws = authenticate()

    # Load configuration from the config.yaml file
    config = load_yaml_config(path="./config.yaml")

    # Register/Load model to/from AzureML Studio
    try:
        # To register a new model
        if config.get("azure").get("to_register_model", False):
            url = config.get("azure").get("pretrained_model_url")
            file_path = config.get("azure").get("model_file_path")
            file_name = config.get("azure").get("model_file")
            alternative_file_name = config.get("azure").get("alternative_model_file")
            model_name = config.get("azure").get("new_model_name")
            # To download and register a pretrained model
            if config.get("azure").get("to_use_pretrained_model", False):
                download_pretrained_model(url=url, file_name=file_name, file_path=file_path)
                model = register_model(ws=ws, model_name=model_name, file_name=file_name, file_path=file_path)
            # To register our own model
            else:
                model = register_model(ws=ws, model_name=model_name, model_file=alternative_file_name, file_path=file_path)
        # To use an already registered model
        else:
            model = Model(workspace=ws, name=config.get("azure").get("registered_model_name"))
    except WebserviceException as e:
        print(e.message)
        print("Please check model's file name, path!")

    # Software Environment
    env_path = config.get("azure").get("env_path")
    env_name = config.get("azure").get("env_name")
    if config.get("azure").get("to_register_env"):
        env = register_environment(ws=ws,
                                   name=env_name,
                                   file_path=env_path)
    else:
        env = get_environment(ws=ws, name=env_name)

    # Scoring Script
    inference_config = config_scoring_script(env=env,
                                             entry_script=config.get("azure").get("scoring_script"))

    # Deployment Configuration
    deployment_config = config_cloud_deployment(cpu_cores=config.get("azure").get("cpu_cores"),
                                                memory_gb=config.get("azure").get("memory_gb"))
    # Deploy
    service = Model.deploy(name=config.get("azure").get("deployed_model_name"),
                           workspace=ws,
                           models=[model],
                           inference_config=inference_config,
                           deployment_config=deployment_config,
                           overwrite=True
                           )
    service.wait_for_deployment(show_output=True)
    # print(service.get_logs())
    return service