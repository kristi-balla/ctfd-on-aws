from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.flags import BaseFlag, FLAG_CLASSES

import boto3

from .ai import request_verdict
import yaml

client = boto3.client("bedrock-runtime", region_name="eu-north-1")

FLAG_NAME = "spontan"


class CustomFlag(BaseFlag):
    name = FLAG_NAME
    templates = {
        "create": "/plugins/my-flag/assets/create.html",
        "update": "/plugins/my-flag/assets/edit.html",
    }

    @staticmethod
    def compare(saved, provided):
        with open("/opt/CTFd/CTFd/plugins/my-flag/qa.yml", "r") as f:
            data = yaml.safe_load(f)

        sources = data["sources"]
        relevant_element = next(
            (item for item in sources if item["key"] == "first-trip"), None
        )
        if not relevant_element:
            return False

        return request_verdict(
            client, relevant_element["question"], provided, relevant_element["solution"]
        )


def load(app):
    FLAG_CLASSES[FLAG_NAME] = CustomFlag
    register_plugin_assets_directory(app, base_path="/plugins/my-flag/assets/")
