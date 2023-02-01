from fastapi.testclient import TestClient

from app.app import app as fastapi_app

client = TestClient(fastapi_app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == [
                                  {
                                    "title": "Todo 1",
                                    "body": "Body 1",
                                    "id": 1,
                                    "author_id": 1
                                  },
                                  {
                                    "title": "Todo Up",
                                    "body": "Body Up",
                                    "id": 2,
                                    "author_id": 1
                                  }
                                ]
