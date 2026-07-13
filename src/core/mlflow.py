import os
from functools import lru_cache

from schemas.agent_schema import AgentTagsInput
from core.config import settings
from core.cli import suppress_mlflow_cli_output

@lru_cache(maxsize=1)
def setup_mlflow():
    import mlflow
    os.environ["MLFLOW_TRACKING_USERNAME"] = settings.MLFLOW_TRACKING_USERNAME
    os.environ["MLFLOW_TRACKING_PASSWORD"] = settings.MLFLOW_TRACKING_PASSWORD.get_secret_value()
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    mlflow.set_workspace(settings.MLFLOW_WORKSPACE_NAME)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
   

    # surpress mlflow logs
    suppress_mlflow_cli_output()

    mlflow.langchain.autolog()


def set_agent_tags(tags: AgentTagsInput) -> None:
    import mlflow
    
    # Required
    mlflow.set_tag("thread_id", tags.thread_id)
    mlflow.set_tag("agent_role", tags.agent_role)

    # Optional
    if tags.job_id:
        mlflow.set_tag("job_id", tags.job_id)
    if tags.task_id:
        mlflow.set_tag("task_id", tags.task_id)