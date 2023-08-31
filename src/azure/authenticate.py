from azureml.core import Workspace

def authenticate():
    try:
        ws = Workspace.from_config()
        print(ws)
        return ws
    except:
        print('Workspace not found')
