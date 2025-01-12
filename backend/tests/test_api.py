import pytest

from tests.setup import mock_client  # noqa: F401


@pytest.fixture(scope="class")
def sample_reading():
    "Sample fixture returns an examplary mass data"
    return {"date": "2025-01-03", "mass": 55.0}

@pytest.fixture(scope="class")
def sample_reading_invalid_mass():
    "Sample fixture returns mass data with invalid mass"
    return {"date": "2025-01-03", "mass": -55.2}

@pytest.fixture(scope="class")
def sample_reading_invalid_date():
    "Sample fixture returns mass data with invalid date"
    return {"date": "2026-02-05", "mass": 55.0}


class TestMassReading:
    def test_post_201(self, mock_client, sample_reading):
        response = mock_client.post("/readings/", json=sample_reading)

        mass_reading = response.json()

        assert response.status_code == 201
        assert mass_reading["date"] == sample_reading["date"]
        assert mass_reading["mass"] == sample_reading["mass"]

    def test_post_invalid_mass(self, mock_client, sample_reading_invalid_mass):
        response = mock_client.post("/readings/", json=sample_reading_invalid_mass)

        assert response.status_code == 422

    def test_post_invalid_date(self, mock_client, sample_reading_invalid_date):
        response = mock_client.post("/readings/", json=sample_reading_invalid_date)

        assert response.status_code == 422        

    def test_list(self, mock_client, sample_reading):
        response = mock_client.get("/readings/")
        
        first_object = response.json()[0]

        assert response.status_code == 200
        assert first_object["date"] == sample_reading["date"]
        assert first_object["mass"] == sample_reading["mass"]

    def test_delete(self, mock_client, sample_reading):
        response = mock_client.delete(
            f"/readings/{sample_reading['date']}/"
        )
        assert response.status_code == 200

    def test_put(self, mock_client, sample_reading):
        post_response = mock_client.post("/readings/", json=sample_reading) 
        assert post_response.status_code == 201

        update_data = {"mass": 76.5}
        response = mock_client.put(
            f"/readings/{sample_reading['date']}/", json=update_data
        )
        assert response.status_code == 200
