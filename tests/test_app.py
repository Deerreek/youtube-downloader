import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"YouTube Downloader" in response.data


def test_download_without_url_returns_error(client):
    response = client.post("/download", data={"url": "", "mode": "audio", "quality": "best"})
    assert response.status_code == 400
    assert response.get_json()["error"]
