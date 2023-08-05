from typing import Dict, Any, List

import pandas

from sktmls import MLSClient, MLSENV, MLSResponse

MLS_META_API_URL = "/api/v1/meta_tables"


class MetaTable:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.schema = kwargs.get("schema")
        self.items = kwargs.get("items")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.user = kwargs.get("user")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MetaItem:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.values = kwargs.get("values")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MetaTableClient(MLSClient):
    """MetaTableClient.

    This is a MetaTableClient is used to call REST APIs related to meta table and meta item with below methods.

    Methods:
        create_meta_table()
        update_meta_table()
        list_meta_tables()
        get_meta_table()
        delete_meta_table()
        create_meta_item()
        update_meta_item()
        list_meta_item()
        get_meta_item()
        delete_meta_item()
    """

    def __init__(
        self, env: MLSENV = None, username: str = None, password: str = None,
    ):
        """Initiate a MetaTableClient object.

        Args:
          env:
            (MLSENV) MLS environment in 'DEV / STG / PRD'. (Default: 'STG')
          username:
            (str) Name of user. (Default: $MLS_USERNAME)
          password:
            (str) Password for user. (Default: $MLS_PASSWORD)

        Returns:
          sktmls.meta_tables.meta_tables.MetaTableClient

        Example:
            meta_table_client = MetaTableClient(env=MLSENV.STG, username={user_name}, password={password})
        """

        super().__init__(env=env, username=username, password=password)

    def create_meta_table(self, name: str, schema: Dict[str, Dict], description: str = None) -> MetaTable:
        """Create a meta table.

        Create a new meta table with name, schema and description if meta table with the name not existing.

        Args:
          name:
            (str) Name of meta table to create.
          schema:
            (dict) Schema of meta table items. (Ex. {"key_value": {"type": "string" or "number"}})
          description:
            Optional; (str) Description of meta table.

        Returns:
          sktmls.meta_tables.meta_tables.MetaTable
            - id: (int) Meta table ID
            - name: (str) Name of meta table
            - description: (str) Description of meta table
            - schema: (dict) Schema of the meta table with item_name and item_type
            - items: (list) List of meta items
            - created_at: (datetime) Created time
            - updated_at: (datetime) Updated time
            - user: (str) Name of creator
        """

        data = {
            "name": name,
            "schema": schema,
        }
        if description:
            data["description"] = description

        return MetaTable(**self._request(method="POST", url=MLS_META_API_URL, data=data).results)

    def update_meta_table(
        self, meta_table: MetaTable, name: str, schema: Dict[str, Dict], description: str = None
    ) -> MLSResponse:
        """Update a existing meta table.

        Update a existing meta table with input args name, schema and description.

        Args:
           meta_table:
            (MetaTable) MetaTable class object.
          name:
            (str) New name of meta table to update.
          schema:
            (dict) New schema of meta table items to update.
          description:
            Optional; (str) New description of meta table to update. If not given, a description of the meta table is changed into None.

        Returns:
          sktmls.meta_tables.meta_tables.MetaTable
            - id: (int) Meta table ID
            - name: (str) Name of meta table
            - description: (str) Description of meta table
            - schema: (dict) Schema of the meta table with item_name and item_type
            - items: (list) List of meta items
            - created_at: (datetime) Created time
            - updated_at: (datetime) Updated time
            - user: (str) Name of creator
        """
        assert type(meta_table) == MetaTable

        data = {
            "name": name,
            "schema": schema,
        }
        if description:
            data["description"] = description

        meta_table.reset(**self._request(method="PUT", url=f"{MLS_META_API_URL}/{meta_table.id}", data=data).results)

        return meta_table

    def get_meta_table(self, id: int = None, name: str = None) -> MetaTable:
        """Get a meta table in detail.

        Get a detailed information of meta table with id / name / description / schema / items / created_dt / updated_at returned as dict type.
        Or Pandas DataFrame format with schema and items.

        Args: One of id or name argument must be provided
          id:
            (int) ID of meta table.
          name:
            (str) Name of meta table.

        Returns:
          sktmls.meta_tables.meta_tables.MetaTable
            - id: (int) Meta table ID
            - name: (str) Name of meta table
            - description: (str) Description of meta table
            - schema: (dict) Schema of the meta table with item_name and item_type
            - items: (list) List of meta items
            - created_at: (datetime) Created time
            - updated_at: (datetime) Updated time
            - user: (str) Name of creator
        """
        assert id or name, "One of id or name must be provided"

        return self.list_meta_tables(id=id, name=name)[0]

    def get_meta_table_dataframe(self, id: int = None, name: str = None) -> pandas.core.frame.DataFrame:
        """Get a meta table in detail in a Pandas DataFrame.

        Get a detailed information of meta table with name / items with Pandas DataFrame format.

        Args: One of id or name argument must be provided
          id:
            (int) ID of meta table.
          name:
            (str) Name of meta table.

        Returns:
          (pandas.core.frame.DataFrame) Meta table items
        """
        assert id or name, "One of id or name must be provided"

        results = self.list_meta_tables(id=id, name=name).get()
        items = results.get("items")

        if items:
            key = pandas.DataFrame.from_records(items)["name"]
            values = pandas.DataFrame.from_records(pandas.DataFrame.from_records(items)["values"])

            return pandas.concat([key, values], axis=1)

    def list_meta_tables(self, **kwargs) -> List[MetaTable]:
        """Get a list of existing meta tables.

        Args:
          kwargs:
            Optional; (dict)
              - id: (int) ID of a meta table.
              - name:  Name of a meta table.

        Returns:
          list(sktmls.meta_tables.meta_tables.MetaTable)
            - id: (int) Meta table ID
            - name: (str) Name of meta table
            - description: (str) Description of meta table
            - schema: (dict) Schema of the meta table with item_name and item_type
            - items: (list) List of meta items
            - created_at: (datetime) Created time
            - updated_at: (datetime) Updated time
        """

        response = self._request(method="GET", url=f"{MLS_META_API_URL}", params=kwargs).results

        if type(response) == list:
            return [MetaTable(**meta_table) for meta_table in response]

        return MetaTable(**response)

    def delete_meta_table(self, meta_table: MetaTable) -> MLSResponse:
        """Delete a meta table.

        Args:
          meta_table:
            (MetaTable) MetaTable class object

        Returns:
          sktmls.MLSResponse
        """
        assert type(meta_table) == MetaTable

        return self._request(method="DELETE", url=f"{MLS_META_API_URL}/{meta_table.id}")

    def create_meta_item(self, meta_table: MetaTable, item_name: str, item_dict: Dict[str, Any]) -> MetaItem:
        """Create a meta item.

        Create a new meta item on a existing meta table with a item_name and values.

        Args:
          meta_table:
            (MetaTable) MetaTable class object.
          item_name:
            (str) Name of meta item to add.
          item_dict:
            (dict) Value of meta item to add.

        Returns:
          sktmls.meta_tables.meta_tables.MetaItem
            - id: (int) ID of a meta item
            - name: (str) Name of a meta item
            - values: (dict) Values of a meta item with meta table schema
        """
        assert type(meta_table) == MetaTable

        data = {"name": item_name, "values": item_dict}

        return MetaItem(
            **self._request(method="POST", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items", data=data).results
        )

    def update_meta_item(
        self, meta_table: MetaTable, meta_item: MetaItem, item_name: Any, item_dict: Dict[str, Any],
    ) -> MetaItem:
        """Update a meta item.

        Update a existing meta item on a existing meta table with item_name and values.

        Args:
          meta_table:
            (MetaTable) MetaTable class object.
          meta_item:
            (MetaItem) MetaItem class object.
          item_name:
            (str) Name of meta item to update.
          item_dict:
            (dict) Value of meta item to update.

        Returns:
          sktmls.meta_tables.meta_tables.MetaItem
            - id: (int) ID of a meta item
            - name: (str) Name of a meta item
            - values: (dict) Values of a meta item with meta table schema
        """
        assert type(meta_table) == MetaTable
        assert type(meta_item) == MetaItem

        data = {"name": item_name, "values": item_dict}

        meta_item.reset(
            **self._request(
                method="PUT", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items/{meta_item.id}", data=data
            ).results
        )

        return meta_item

    def list_meta_items(self, meta_table: MetaTable, **kwargs) -> List[MetaItem]:
        """Get a list of meta item existing on a meta table.

        Args:
          meta_table:
            (MetaTable) MetaTable class object.
          kwargs:
            Optional; (dict)
              - id: (int) ID of a meta item.
              - name:  Name of a meta item.

        Returns:
          list(sktmls.meta_tables.meta_tables.MetaItem)
            - id: (int) ID of a meta item
            - name: (str) Name of a meta item
            - values: (dict) Values of a meta item with meta table schema
        """
        assert type(meta_table) == MetaTable

        response = self._request(
            method="GET", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items", params=kwargs
        ).results

        if type(response) == list:
            return [MetaItem(**meta_item) for meta_item in response]

        return MetaItem(**response)

    def get_meta_item(self, meta_table: MetaTable, id: int = None, name: str = None) -> MetaItem:
        """Get a meta item.

        Get a existing meta item in detail.

        Args: One of id or name argument must be provided
          meta_table:
            (MetaTable) MetaTable class object.
          id:
            (int) ID of meta item.
          name:
            (str) Name of meta item.

        Returns:
          sktmls.meta_tables.meta_tables.MetaItem
            - id: (int) ID of a meta item
            - name: (str) Name of a meta item
            - values: (dict) Values of a meta item with meta table schema
        """
        assert type(meta_table) == MetaTable
        assert id or name, "One of id or name must be provided"

        return self.list_meta_item(meta_table, id=id, name=name)

    def delete_meta_item(self, meta_table: MetaTable, meta_item: MetaItem) -> MLSResponse:
        """Delete a meta item.

        Args:
          meta_table:
            (MetaTable) MetaTable class object.
          meta_item:
            (MetaItem) MetaItem class object.

        Returns:
          sktmls.MLSResponse
        """
        assert type(meta_table) == MetaTable
        assert type(meta_item) == MetaItem

        return self._request(method="DELETE", url=f"{MLS_META_API_URL}/{meta_table.id}/meta_items/{meta_item.id}")
