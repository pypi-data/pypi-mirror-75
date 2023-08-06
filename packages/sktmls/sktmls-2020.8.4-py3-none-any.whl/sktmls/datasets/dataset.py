from dateutil import parser
from enum import Enum
from string import Template
from typing import Any, List

from sktmls import MLSClient, MLSENV, MLSResponse
from sktmls.config import config

SPARK_QUERY_FOR_LABLE_DATA = Template(
    """
SELECT sha2(source.svc_mgmt_num, 256) AS svc_mgmt_num, source.period AS period
FROM (
    ${source_query}
) AS source
"""
)


class ProblemType(Enum):
    """
    Problem type.
    """

    SCORE = "score"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class DatasetError(Exception):
    def __init__(self, *args, **kwargs):
        """
        Create a new DatasetError.
        """
        super().__init__(*args, **kwargs)


class FeatureStoreConf:
    def __init__(self, enabled: bool, feature_group_id_list: List[int] = None, n_label_ratio: float = 1.0):
        """
        Feature store configuration for creating a new dataset.

        Args:
            enabled: (bool) Whether using feature store or not.
            feature_group_id_list: (list(int)) List of feature store id.
            n_label_ratio: (float) Ratio of the 'N' label for the score type problem.
        """
        self.enabled = enabled
        self.feature_group_id_list = feature_group_id_list
        self.n_label_ratio = n_label_ratio

    def __str__(self) -> str:
        return str(self.__dict__)


class LabelDataConf:
    def __init__(self, source_type: str, source_path: str):
        """
        Label data configuration for creating a new dataset.

        Args:
            source_type: (str) Whether using feature store or not.
            source_path: (str) List of feature store id.
        """
        self.source_type = source_type
        self.source_path = source_path

    def __str__(self) -> str:
        return str(self.__dict__)


class Dataset:
    def __init__(self, **kwargs):
        """
        Automl Dataset.

        Attributes:
            id: (int) Dataset ID.
            name: (str) Dataset name.
            status: (str) Dataset status.
            problem_type: (sktmls.datasets.ProblemType) Problem type of the dataset.
            feature_store_conf: (sktmls.datasets.FeatureStoreConf) Feature store configuration of the dataset.
            label_data_conf: (sktmls.datasets.LabelDataConf) Label data configuration of the dataset.
            created_at: (datetime.datetime) Datetime when the dataset is created.
            updated_at: (datetime.datetime) Datetime when the dataset is lastly updated.
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.status = kwargs.get("status")
        self.problem_type = ProblemType(kwargs.get("data_type"))

        base_feature_conf = kwargs.get("setup_conf", {}).get("base_feature_conf", {})
        self.feature_store_conf = FeatureStoreConf(
            enabled=base_feature_conf.get("enabled"),
            feature_group_id_list=base_feature_conf.get("feature_group_id_list"),
            n_label_ratio=base_feature_conf.get("n_label_ratio"),
        )

        label_data_conf = kwargs.get("setup_conf", {}).get("label_data_conf", {})
        self.label_data_conf = LabelDataConf(
            source_type=label_data_conf.get("source_type"), source_path=label_data_conf.get("source_path"),
        )

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return self.name


class DatasetClient(MLSClient):
    def __init__(self, env: MLSENV = None, username: str = None, password: str = None):
        """
        Create a new dataset client.

        Args:
            env: (MLSENV) MLS Environment.
            username: (str) MLS username.
            password: (str) MLS password.
        """
        super().__init__(env=env, username=username, password=password)

    def create_dataset(
        self, name: str, problem_type: ProblemType, feature_store_conf: FeatureStoreConf, label_data_conf: LabelDataConf
    ) -> MLSResponse:
        """
        Create a new dataset.

        Args:
            name: (str) Dataset name.
            problem_type: (ProblemType) Type of the problem.
            feature_store_conf: (FeatureStoreConf) Feature store configuration.
            label_data_conf: (LabelDataConf) Label data configuration.
        """
        data = {
            "name": name,
            "type": problem_type.value,
            "base_feature_conf": feature_store_conf.__dict__,
            "label_data_conf": label_data_conf.__dict__,
        }
        return self._request(method="POST", url="api/v1/datasets", data=data)

    def list_datasets(self, **kwargs) -> List[Dataset]:
        """
        List datasets.

        Args:
          kwargs:
            Optional; (dict)
              - id: (int) Dataset ID.
              - name: (str) Dataset name.

        Returns:
          list(sktmls.datasets.Dataset)
        """
        response = self._request(method="GET", url="api/v1/datasets", params=kwargs)

        if response.code != 0:
            raise DatasetError(f"Fail to search datasets: {response.error}")

        return [Dataset(**dataset) for dataset in response.results]

    def get_dataset(self, name: str = None, id: int = None) -> Dataset:
        assert id is not None or name, "One of id or name must be provided"

        datasets = self.list_datasets(name=name, id=id)

        if len(datasets) == 0:
            raise DatasetError("Dataset does not exists")

        return datasets[0]

    def delete_dataset(self, name: str = None, id: int = None) -> None:
        dataset = self.get_dataset(name=name, id=id)
        response = self._request(method="DELETE", url=f"api/v1/datasets/{dataset.id}")

        if response.code != 0:
            raise DatasetError(f"Fail to delete a dataset: {response.error}")

    def upload_label_data_from_ye(self, spark_session: Any, output_name: str, source_query: str) -> None:
        """
        Upload a label data using a spark query with a hive table.

        Args:
            spark_session: (SparkSession) Spark session from the skt.ye.get_spark() function.
            output_name: (str) Name of the output data.
            source_query: (str) Spark query for querying the hive table.
        """
        assert type(spark_session).__name__ == "SparkSession", "Invalid type of spark_session"
        assert type(output_name) == str, "Invalid type of output_name"
        assert type(source_query) == str, "Invalid type of source_query"

        if not config.MLS_RUNTIME_ENV == "YE":
            raise DatasetError("upload_label_data_from_ye() is only supported over the YE environment.")

        query = SPARK_QUERY_FOR_LABLE_DATA.substitute(source_query=source_query)
        target_path = f"gs://sktmls-automl-{self.get_env().value}/{self.get_username()}/label_data_ye/{output_name}"
        spark_session.sql(query).write.mode("overwrite").csv(target_path, header=True)
        spark_session.stop()
