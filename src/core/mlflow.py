import mlflow

from schemas.agent_schema import AgentTagsInput
from core.config import settings
from core.cli import suppress_mlflow_cli_output


def setup_mlflow():
    import mlflow

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)

    # surpress mlflow logs
    suppress_mlflow_cli_output()

    mlflow.langchain.autolog()


def set_agent_tags(tags: AgentTagsInput) -> None:

    # Required
    mlflow.set_tag("thread_id", tags.thread_id)
    mlflow.set_tag("agent_role", tags.agent_role)

    # Optional
    if tags.job_id:
        mlflow.set_tag("job_id", tags.job_id)
    if tags.task_id:
        mlflow.set_tag("task_id", tags.task_id)