import sys

from deployment import *
import mlflow

# run test job
from databricks_cli.configure.provider import get_config
from databricks_cli.configure.config import _get_api_client

model_name, exp_path, cloud = read_config()

try:
    mlflow.set_experiment(exp_path)
except Exception as e:
    raise Exception(f"""{e}.
    Have you added the following secrets to your github repo?
        secrets.DATABRICKS_HOST
        secrets.DATABRICKS_TOKEN""")

libraries = prepare_libraries()
run_id, artifact_uri = log_artifacts(model_name, libraries)

# run test job
apiClient = _get_api_client(get_config())

res = submit_jobs(apiClient, 'dev-tests', artifact_uri, libraries, cloud)
if not res:
    print('Tests were not successful. Quitting..')
    sys.exit(-100)
