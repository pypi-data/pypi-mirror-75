import base64
import json
import os
import requests
from typing import Any

from sktmls import MLSENV
from sktmls.config import config


class MLSClientError(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg


class MLSResponse:
    def __init__(self, response: requests.models.Response):
        data = json.loads(response.content.decode("utf-8"))
        self.status = response.status_code
        self.code = data.get("code")
        self.error = data.get("error")
        self.results = data.get("results")

        if self.error:
            raise MLSClientError(code=self.code, msg=self.error)


class MLSClient:
    def __init__(self, env: MLSENV = None, username: str = None, password: str = None):
        if env:
            assert env in MLSENV.list_items(), "Invalid environment."
            self.__env = env
        elif os.environ.get("MLS_ENV"):
            self.__env = os.environ["MLS_ENV"]
        else:
            self.__env = MLSENV.STG

        if username:
            assert type(username) == str, "Invalid type of username"
            self.__username = username
        elif os.environ.get("MLS_USERNAME"):
            self.__username = os.environ["MLS_USERNAME"]
        else:
            raise MLSClientError(
                code=400, msg="'username' must be provided with parameter or environment variable (MLS_USERNAME)"
            )

        if password:
            assert type(password) == str, "Invalid type of password"
            self.__password = password
        elif os.environ.get("MLS_PASSWORD"):
            self.__password = os.environ["MLS_PASSWORD"]
        else:
            raise MLSClientError(
                code=400, msg="'password' must be provided with parameter or environment variable (MLS_PASSWORD)"
            )

        self.__api_token = base64.b64encode(f"{self.__username}:{self.__password}".encode()).decode("utf-8")

    def get_env(self) -> MLSENV:
        return self.__env

    def get_username(self) -> str:
        return self.__username

    def _request(self, method: str, url: str, data: Any = None, params=None) -> MLSResponse:
        response = requests.request(
            method=method,
            url=f"{config.MLS_API_URL[self.__env.value]}{'' if url.startswith('/') else '/'}{url}",
            headers={"Authorization": f"Basic {self.__api_token}"},
            json=data,
            params=params,
        )

        return MLSResponse(response)
