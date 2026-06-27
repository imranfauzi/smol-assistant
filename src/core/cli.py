import os
import logging
from core.config import settings

def suppress_mlflow_cli_output() -> None:
    os.environ.setdefault("MLFLOW_SUPPRESS_PRINTING_URL_TO_STDOUT", settings.MLFLOW_SUPPRESS_PRINTING_URL_TO_STDOUT)
    os.environ.setdefault("MLFLOW_LOGGING_LEVEL", settings.MLFLOW_LOGGING_LEVEL)

    logging.getLogger("mlflow").setLevel(logging.ERROR)
    logging.getLogger("mlflow.tracing").setLevel(logging.ERROR)
    logging.getLogger("mlflow.tracing.export.async_export_queue").setLevel(
        logging.ERROR
    )