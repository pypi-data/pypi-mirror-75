from sktmls.models.contrib import ShuffleListModel


class TestShuffleListModel:
    def test_000_shuffle_list(self):
        slm = ShuffleListModel("test_model", "test_version", "item001", "item001_name", ["h", "e", "l", "o", "w"])

        results = slm.predict(None)
        assert "items" in results
        items = results["items"]

        assert items.get("id") == "item001"
        assert items.get("name") == "item001_name"
        assert "props" in items
        assert type(items.get("props").get("item001")) == list
        assert set(items.get("props").get("item001")) == {"h", "e", "l", "o", "w"}
