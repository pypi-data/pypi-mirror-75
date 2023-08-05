import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import List, TYPE_CHECKING

import joblib

from sktmls import MLSENV
from sktmls.config import config

if TYPE_CHECKING:
    from sktmls.models import MLSModel

MLS_MODEL_DIR = Path.home().joinpath("models")
MODEL_BINARY_NAME = "model.joblib"
MODEL_META_NAME = "model.json"
BUCKET = "mls-model-registry"


class ModelRegistryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelRegistry:
    def __init__(self, env: MLSENV = None):
        """
        Init a ModelRegistry instance

        Args:
            env: (MLSENV) AWS ENV.
        """
        if env:
            assert env in MLSENV.list_items(), "Invalid environment."
            self.__env = env
        elif os.environ.get("MLS_ENV"):
            self.__env = os.environ["MLS_ENV"]
        else:
            self.__env = MLSENV.STG

    def save(self, mls_model: "MLSModel", force: bool = False) -> None:
        """
        Upload model_binary (model.joblib) and model_meta (model.json) to MLS model registry.
        Equivalent to MLSModel.save method.

        Args:
            mls_model: (MLSModel) Model instance declared with class inheriting MLSModel.
            force: (bool) Force to overwrite model files on S3 if exists.

        Example:
            model_registry = ModelRegistry(env=MLSENV.STG)
            model_registry.save(gbm_model)
        """
        model_path = MLS_MODEL_DIR.joinpath(mls_model.model_name, mls_model.model_version)
        model_binary_path = model_path.joinpath(MODEL_BINARY_NAME)
        model_meta_path = model_path.joinpath(MODEL_META_NAME)

        model_path.mkdir(parents=True, exist_ok=True)
        joblib.dump(mls_model, model_binary_path)
        with model_meta_path.open("w") as f:
            json.dump(
                {
                    "name": mls_model.model_name,
                    "version": mls_model.model_version,
                    "model_lib": mls_model.model_lib,
                    "model_lib_version": mls_model.model_lib_version,
                    "model_data": f"/models/{mls_model.model_name}/{mls_model.model_version}/{MODEL_BINARY_NAME}",
                    "features": mls_model.features,
                    "class": mls_model.__class__.__name__,
                },
                f,
            )

        if config.MLS_RUNTIME_ENV == "LOCAL":
            return

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"{s3_path}/{mls_model.model_name}/{mls_model.model_version}"

        force_option = "-f" if force else ""
        process_mkdir = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -mkdir -p s3a://{s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process_mkdir.wait()
        if process_mkdir.returncode != 0:
            raise ModelRegistryError(f"Making Directory on S3 ({s3_path}) is FAILED")

        process_model_binary = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -put {force_option} {model_binary_path} s3a://{s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process_model_binary.wait()
        if process_model_binary.returncode != 0:
            raise ModelRegistryError(f"Loading model_binary(model.joblib) to S3 ({s3_path}) is FAILED.")

        process_model_meta = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -put {force_option} {model_meta_path} s3a://{s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process_model_meta.wait()
        if process_model_meta.returncode != 0:
            raise ModelRegistryError(f"Loading model_meta(meta.json) to S3 ({s3_path}) is FAILED")

    def list_models(self) -> List[str]:
        """
        List all registered models in model registry.

        Returns:
            list(str): Names of existing models.

        Example:
            model_registry = ModelRegistry(env=MLSENV.STG)
            model_names = model_registry.list_models()
        """
        if config.MLS_RUNTIME_ENV == "LOCAL":
            return [x.name for x in MLS_MODEL_DIR.iterdir() if x.is_dir()]

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"

        s3_path = f"s3a://{s3_path}/"
        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -ls {s3_path}"), stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"Listing models in ({s3_path}) is FAILED.")

        output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
        return output

    def list_versions(self, model_name: str) -> List[str]:
        """
        List all registered model versions for a model.

        Args:
            model_name: (str) Name of model.

        Returns:
            list(str): Versions of the given model.

        Example:
            model_registry = ModelRegistry(env=MLSENV.STG)
            model_versions = model_registry.list_versions("hello_model")
        """
        if config.MLS_RUNTIME_ENV == "LOCAL":
            return [x.name for x in MLS_MODEL_DIR.joinpath(model_name).iterdir() if x.is_dir()]

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"s3a://{s3_path}/{model_name}/"

        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -ls {s3_path}"), stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"Listing versions in ({s3_path}) is FAILED.")

        output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
        return output

    def load(self, model_name: str, model_version: str) -> "MLSModel":
        """
        Get a model instance from model registry.

        Args:
            model_name: (str) Model name
            model_version: (str) Model version

        Returns:
            sktmls.models.mls_model.MLSModel: Instance of MLSModel.

        Example:
            model_registry = ModelRegistry(env=MLSENV.STG)
            hello_model_v1 = model_registry.load(model_name="hello_model", model_version="v1")
            results = hello_model_v1.predict([1, 2, 3])
        """
        model_path = MLS_MODEL_DIR.joinpath(model_name, model_version)
        model_binary_path = model_path.joinpath(MODEL_BINARY_NAME)

        if config.MLS_RUNTIME_ENV == "LOCAL":
            return joblib.load(model_binary_path)

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"s3a://{s3_path}/{model_name}/{model_version}/{MODEL_BINARY_NAME}"

        model_path.mkdir(parents=True, exist_ok=True)

        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {config.HDFS_OPTIONS} -get {s3_path} {model_binary_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"Getting model from ({s3_path}) is FAILED.")

        return joblib.load(model_binary_path)
