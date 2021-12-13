import io
import logging
from os import environ

import boto3

from prmexporter.config import SpineExporterConfig
from prmexporter.io.http_client import HttpClient
from prmexporter.io.json_formatter import JsonFormatter
from prmexporter.io.secret_manager import SsmSecretManager

logger = logging.getLogger("prmexporter")


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


VERSION = "v3"


def main():
    _setup_logger()

    config = SpineExporterConfig.from_environment_variables(environ)

    ssm = boto3.client("ssm")
    secret_manager = SsmSecretManager(ssm)
    splunk_api_token = secret_manager.get_secret(config.splunk_api_token_param_name)

    http_client = HttpClient(url=config.splunk_url)

    data = {
        "output_mode": "csv",
        "earliest_time": 1638835200,
        "latest_time": 1638921600,
        "search": """search index=\"spine2vfmmonitor\" service=\"gp2gp\" logReference=\"MPS0053d\"
        | head 1
        | table _time, conversationID, GUID, interactionID, messageSender,
        messageRecipient, messageRef, jdiEvent, toSystem, fromSystem""",
    }

    api_response_content = http_client.fetch_data(auth_token=splunk_api_token, request_body=data)

    s3 = boto3.resource("s3")
    s3_spine_output_data_bucket = s3.Bucket(name=config.output_spine_data_bucket)

    s3_spine_output_data_bucket.upload_fileobj(
        io.BytesIO(api_response_content), f"{VERSION}/test-spine-data.csv"
    )


if __name__ == "__main__":
    main()
