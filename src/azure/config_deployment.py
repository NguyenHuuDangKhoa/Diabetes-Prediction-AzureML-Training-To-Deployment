from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice

def config_local_deployment(port: int) -> LocalWebservice:
    """
    Configurate the deployment of a model
    :param port: port for connect to the local host
    :return: a configurated local web service
    """
    deployment_config = LocalWebservice.deploy_configuration(port=port)
    return deployment_config

def config_cloud_deployment(cpu_cores: int, memory_gb: int, auth_enabled=True) -> AciWebservice:
    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores=cpu_cores,
        memory_gb=memory_gb,
        auth_enabled=auth_enabled)
    return deployment_config