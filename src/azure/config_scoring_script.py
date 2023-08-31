# A class to define the configuration for deploying models as web services
from azureml.core.model import InferenceConfig
from azureml.core import Environment

def config_scoring_script(env: Environment, entry_script: str, source_directory: str) -> InferenceConfig:
    """
    Configurate the scoring script
    :param env: an environment that would be used for deployment
    :param entry_script: the scoring script to evalute the model prediction
    :param source_directory: path to the scoring script
    :return: a configurated script for evaluating model prediction
    """
    inference_config = InferenceConfig(environment=env, source_directory=source_directory, entry_script=entry_script)
    return inference_config
