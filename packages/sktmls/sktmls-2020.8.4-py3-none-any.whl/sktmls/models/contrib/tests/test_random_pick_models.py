from sktmls.models.contrib import RandomPickModel


class TestRandomPickModel:
    def test_000_random_pick_1(self):
        rpm = RandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ],
            num_pick=1,
        )

        assert rpm.predict(None) in [
            {"items": [{"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}}]},
            {"items": [{"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}}]},
        ]

    def test_000_random_pick_2(self):
        rpm = RandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ],
            num_pick=2,
        )

        result = rpm.predict(None)
        assert result == {
            "items": [
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ]
        } or result == {
            "items": [
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
            ]
        }
