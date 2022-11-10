from app import app
import pytest

@pytest.fixture()
def client():
    return app


def test_api_posts(client):
    response = app.test_client().get("/api/posts")
    assert response.status_code == 200