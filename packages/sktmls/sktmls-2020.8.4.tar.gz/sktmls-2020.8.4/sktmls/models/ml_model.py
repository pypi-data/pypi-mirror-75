from typing import List
from enum import Enum

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSClientError
from sktmls.datasets import Dataset

MLS_MODELS_API_URL = "/api/v1/models"


class MLModel:
    """
    ML모델 클래스 입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - version: (str) ML모델 버전
            - creator: (str) ML모델 생성 계정명
            - description: (str) ML모델 설명
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - table: (str) ML모델 테이블
            - model_data: (str) ML모델 데이터
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.models.MLModel`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.version = kwargs.get("version")
        self.description = kwargs.get("description")
        self.creator = kwargs.get("creator")
        self.model_type = kwargs.get("model_type")
        self.table = kwargs.get("table")
        self.model_data = kwargs.get("model_data")
        self.status = kwargs.get("status")
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

    def get(self) -> dict:
        return self.__dict__


class AutoMLModel(MLModel):
    """
    AutoML모델 클래스 입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - version: (str) ML모델 버전
            - description: (str) ML모델 설명
            - creator: (str) ML모델 생성 계정명
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - model_meta: (dict) ML모델 메타정보
            - components: (dict) ML모델 컴포넌트
            - dataset_id: (int) ML 데이터셋 고유 ID
            - dataset_name: (str) ML 데이터셋 이름
            - automl_model_info: (dict) AutoML모델 정보

        ## Returns
        `sktmls.models.AutoMLModel`
        """

        super().__init__(**kwargs)
        self.dataset_id = kwargs.get("dataset_id")
        self.dataset_name = kwargs.get("dataset_name")
        self.automl_model_info = kwargs.get("automl_model_info")


class ManualModel(MLModel):
    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - model_type: (str) ML모델 타입 (`automl` | `manual`)
            - version: (str) ML모델 버전
            - description: (str) ML모델 설명
            - creator: (str) ML모델 생성 계정명
            - status: (`sktmls.models.MLModelStatus`) ML모델 상태
            - model_meta: (dict) ML모델 메타정보
            - components: (dict) ML모델 컴포넌트
            - table: (str) ML모델 테이블
            - model_lib: (str) ML모델 라이브러리
            - model_data: (str) ML모델 데이터
            - features: (str) ML모델에 사용된 피쳐
            - is_enabled: (bool) 활성상태 여부

        ## Returns
        `sktmls.models.ManualModel`
        """

        super().__init__(**kwargs)
        self.model_meta = kwargs.get("model_meta")
        self.components = kwargs.get("components")
        self.model_lib = kwargs.get("model_lib")
        self.features = kwargs.get("features")
        self.is_enabled = kwargs.get("is_enabled")


class MLModelStatus(Enum):
    IN_USE = "IN_USE"
    NOT_IN_USE = "NOT_IN_USE"
    AUTOML_TRAINING = "TRAINING"
    AUTOML_DONE = "DONE"
    AUTOML_FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class MLModelClient(MLSClient):
    def __init__(self, env: MLSENV = None, username: str = None, password: str = None):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.models.MLModelClient`

        ## Example

        ```
        ml_model_client = MLModelClient(env=MLSENV.STG, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, username=username, password=password)

    def create_automl_model(
        self, dataset: Dataset, model_name: str, model_version: str, description: str
    ) -> AutoMLModel:
        """
        AutoML 모델을 생성합니다.

        ## Args

        - dataset: (sktmls.datasets.Dataset) ML 데이터셋
        - model_name: (str) 생성할 AutoML 이름
        - model_version: (str) 생성할 AutoML 버전
        - description: (str) 생성할 AutoML 설명

        ## Returns
        `sktmls.models.AutoMLModel`

        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - creator: (str) ML모델 생성 계정명
        - description: (str) ML모델 설명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: (dict) ML모델 컴포넌트
        - dataset_id: (int) ML 데이터셋 고유 ID
        - dataset_name: (str) ML 데이터셋 이름
        - automl_model_info: (dict) AutoML모델 정보

        ## Example

        ```
        automl_model = ml_model_client.create_automl_model(
            dataset=dataset,
            model_name="automl_test_model",
            model_version="v1",
            description='test_model'
        )
        ```
        """
        assert type(dataset) == Dataset

        data = {
            "model_type": "automl",
            "name": model_name,
            "version": model_version,
            "description": description,
            "dataset_id": dataset.id,
        }
        response = self._request(method="POST", url=MLS_MODELS_API_URL, data=data).results
        return self.get_ml_model(id=response.get("id"))

    def list_ml_models(self, **kwargs) -> List[MLModel]:
        """
        ML모델 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 필터 조건
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - version: (str) ML모델 이름

        ## Returns
        list(`sktmls.models.Model`)

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 버전
        - creator: (str) ML모델 생성 계정명
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - table: (str) ML모델 테이블
        - model_data: (str) ML모델 데이터
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```
        ml_models = ml_model_client.list_ml_models()
        ```
        """
        response = self._request(method="GET", url=MLS_MODELS_API_URL, params=kwargs)
        return [MLModel(**ml_model) for ml_model in response.results]

    def get_automl_model(self, id: int = None, name: str = None, version: str = None) -> AutoMLModel:
        """
        AutoML모델 정보를 가져옵니다.

        ## Args: `id` 또는 (`name` and `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 이름

        ## Returns
        `sktmls.models.AutoMLModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: (dict) ML모델 컴포넌트
        - dataset_id: (int) ML 데이터셋 고유 ID
        - dataset_name: (str) ML 데이터셋 이름
        - automl_model_info: (dict) AutoML모델 정보

        ## Example

        ```
        ml_model_by_id = ml_model_client.get_automl_model(id=3)
        ml_model_by_name_and_version = ml_model_client.get_automl_model(name="my_automl_model", version="my_automl_version")
        ```
        """
        assert id or (name and version), "`id` 또는 (`name`, `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        ml_models = self.list_ml_models(id=id, name=name, version=version)
        if len(ml_models) == 0:
            raise MLSClientError(code=404, msg="ML모델이 없습니다.")
        elif len(ml_models) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 모델이 여러개 존재합니다.")

        if ml_models[0].model_type != "automl":
            raise MLSClientError(code=401, msg="AutoML 모델이 아닙니다.")

        return AutoMLModel(**self._request(method="GET", url=f"{MLS_MODELS_API_URL}/{ml_models[0].id}").results)

    def get_manual_model(self, id: int = None, name: str = None, version: str = None) -> ManualModel:
        """
        Manual모델 정보를 가져옵니다.

        ## Args: `id` 또는 (`name` and `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - version: (str) ML모델 이름

        ## Returns
        `sktmls.models.ManualModel`

        - id: (int) ML모델 고유 ID
        - name: (str) ML모델 이름
        - model_type: (str) ML모델 타입 (`automl` | `manual`)
        - version: (str) ML모델 버전
        - description: (str) ML모델 설명
        - creator: (str) ML모델 생성 계정명
        - status: (`sktmls.models.MLModelStatus`) ML모델 상태
        - model_meta: (dict) ML모델 메타정보
        - components: (dict) ML모델 컴포넌트
        - table: (str) ML모델 테이블
        - model_lib: (str) ML모델 라이브러리
        - model_data: (str) ML모델 데이터
        - features: (str) ML모델에 사용된 피쳐
        - is_enabled: (bool) 활성상태 여부

        ## Example

        ```
        ml_model_by_id = ml_model_client.get_manual_model(id=3)
        ml_model_by_name_and_version = ml_model_client.get_manual_model(name="my_manual_model", version="my_manual_version")
        ```
        """
        assert id or (name and version), "`id` 또는 (`name`, `version`) 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        ml_models = self.list_ml_models(id=id, name=name, version=version)
        if len(ml_models) == 0:
            raise MLSClientError(code=404, msg="ML모델이 없습니다.")
        elif len(ml_models) > 1:
            raise MLSClientError(code=409, msg="같은 이름의 모델이 여러개 존재합니다.")

        if ml_models[0].model_type != "manual":
            raise MLSClientError(code=401, msg="Manual 모델이 아닙니다.")

        return ManualModel(**self._request(method="GET", url=f"{MLS_MODELS_API_URL}/{ml_models[0].id}").results)
