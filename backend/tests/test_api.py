import pytest

from tests.setup import mock_client  # noqa: F401


@pytest.fixture(scope="class")
def sample_reading_data():
    "Sample fixture returns an examplary mass data"
    return {"date": "2025-01-03", "mass": 5.0}


class TestMassReading:
    def test_post(self, mock_client, sample_reading_data):
        response = mock_client.post("/readings/", json=sample_reading_data)
        assert response.status_code == 201

        mass_reading = response.json()
        print(mass_reading)

        assert mass_reading["date"] == sample_reading_data["date"]
        assert mass_reading["mass"] == sample_reading_data["mass"]

    def test_list(self, mock_client, sample_reading_data):
        response = mock_client.get("/readings/")
        assert response.status_code == 200

        first_object = response.json()[0]

        assert first_object["date"] == sample_reading_data["date"]
        assert first_object["mass"] == sample_reading_data["mass"]

    def test_delete(self, mock_client, sample_reading_data):
        delete_response = mock_client.delete(
            f"/readings/{sample_reading_data['date']}/"
        )
        assert delete_response.status_code == 200

    def test_put(self, mock_client, sample_reading_data):
        update_data = {"mass": 76.5}
        response = mock_client.put(
            f"/readings/{sample_reading_data['date']}/", json=update_data
        )
        assert response.status_code == 200
