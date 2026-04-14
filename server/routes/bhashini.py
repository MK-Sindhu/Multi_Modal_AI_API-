import asyncio
from typing import List, Union
from wave import Error
import requests

from dotenv import load_dotenv
import os

load_dotenv()

ulca_user_id = os.getenv("ULCA_USER_ID")
ulca_api_key = os.getenv("ULCA_API_KEY")
meity_pipeline_id = os.getenv("MEITY_PIPELINE_ID")

BASE_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

headers = {"userID": ulca_user_id, "ulcaApiKey": ulca_api_key}


class Vaani:
    def __init__(self, tasks, keys=None, pipeline_id=None) -> None:
        self.BASE_URL = (
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        )
        if keys:
            self.ulca_api_key = keys["ULCA_API_KEY"]
            self.ulca_user_id = keys["USER_ID"]
        else:
            try:
                self.ulca_api_key = os.environ["ULCA_API_KEY"]
                self.ulca_user_id = os.environ["ULCA_USER_ID"]
            except KeyError:
                raise KeyError(
                    "Provide ULCA_API_KEY and USER_ID as env variable pr pass it as dictionary, namely keys"
                )
        self.tasks = []
        self.pipeline_config = None
        if type(tasks) == str:
            self.tasks.append(tasks)
        else:
            self.tasks = tasks

        self.pipeline_id = pipeline_id
        if not self.pipeline_id:
            self.pipeline_id = meity_pipeline_id

        self.source_language = ""
        self.target_language = ""

        self.gender = "male"

        if pipeline_id:
            self.pipeline_id = pipeline_id
        self._headers = {"ulcaApiKey": self.ulca_api_key, "userID": self.ulca_user_id}
        if not self.ulca_api_key or not self.ulca_user_id:
            raise Error("Please set the ULCA_API_KEY and USER_ID environment variables")

    def set_pipeline_config(
        self, source_language: str, target_language: Union[str, List] = ""
    ):
        payload = self._get_payload(self.tasks, source_language, target_language)

        response = requests.post(self.BASE_URL, headers=self._headers, json=payload)

        self.source_language = source_language
        if target_language:
            self.target_language = target_language

        if response.ok:
            self.pipeline_config = response.json()
            self._set_inference_config()
        else:
            raise Error(response.status_code, response.text)

    def _set_inference_config(self):
        # Inference config
        self.inference_api_url = self.pipeline_config["pipelineInferenceAPIEndPoint"][
            "callbackUrl"
        ]
        self.inference_soc_url = self.pipeline_config[
            "pipelineInferenceSocketEndPoint"
        ]["callbackUrl"]
        self.inference_api_key = self.pipeline_config["pipelineInferenceAPIEndPoint"][
            "inferenceApiKey"
        ]
        self.authorization = {
            self.inference_api_key["name"]: self.inference_api_key["value"]
        }

    def _get_payload(
        self, tasks: List, source_language: str = "", target_language: str = ""
    ):
        payload = {"pipelineTasks": []}

        for task in tasks:
            payload["pipelineTasks"].append(
                {
                    "taskType": task,
                    "config": {
                        "language": {
                            "sourceLanguage": source_language,
                        }
                    },
                }
            )
            if task == "translation":
                payload["pipelineTasks"][-1]["config"]["language"]["targetLanguage"] = (
                    target_language
                )
            if task == "tts" and "translation" in tasks:
                payload["pipelineTasks"][-1]["config"]["language"]["sourceLanguage"] = (
                    target_language
                )

        payload["pipelineRequestConfig"] = {"pipelineId": self.pipeline_id}
        return payload

    def _get_inference_payload(self):
        payload = {"pipelineTasks": []}
        for task in self.pipeline_config["pipelineResponseConfig"][:]:
            payload["pipelineTasks"].append(
                {
                    "taskType": task["taskType"],
                    "config": {
                        "language": {
                            "sourceLanguage": task["config"][0]["language"][
                                "sourceLanguage"
                            ],
                        },
                        "serviceId": task["config"][0]["serviceId"],
                    },
                }
            )
            if task["taskType"] == "asr":
                payload["pipelineTasks"][-1]["config"]["audioFormat"] = "wav"
                payload["pipelineTasks"][-1]["config"]["samplingRate"] = 16000

            if task["taskType"] == "translation":
                payload["pipelineTasks"][-1]["config"]["language"]["targetLanguage"] = (
                    task["config"][0]["language"]["targetLanguage"]
                )

            # specify gender if task is tts
            if task["taskType"] == "tts":
                payload["pipelineTasks"][-1]["config"]["gender"] = self.gender

        payload["inputData"] = {}
        return payload

    async def inference(self, inputs, source_language, target_language=""):
        if self.source_language != source_language:
            self.set_pipeline_config(source_language, target_language=target_language)

        payload = self._get_inference_payload()

        if "asr" in self.tasks:
            payload["inputData"]["audio"] = [{"audioContent": inputs}]
        else:
            payload["inputData"]["input"] = [{"source": inputs}]

        self.inference_payload = payload
        response = requests.post(
            self.inference_api_url, headers=self.authorization, json=payload
        )
        if response.ok:
            data = response.json()
            self.inferred_data = data
            return data
        else:
            raise Error(f"{response.status_code}: {response.text}")

    async def translation(self, text, source_language, target_language):
        if self.source_language != source_language:
            self.set_pipeline_config(
                source_language=source_language, target_language=target_language
            )
        resp = await self.inference(
            text, source_language, target_language=target_language
        )
        return resp

    async def tts(self, text, source_language, gender="male"):
        self.gender = gender
        if self.source_language != source_language:
            self.set_pipeline_config(source_language=source_language)
        resp = await self.inference(text, source_language)
        return resp
