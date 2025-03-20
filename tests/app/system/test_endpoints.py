from fastapi import FastAPI
from starlette.testclient import TestClient

API_PATH = "/api/system"


def test_get_readiness(app: FastAPI, client: TestClient) -> None:
    response = client.get(API_PATH + "/readiness")
    assert response.status_code == 200


def test_get_liveness(app: FastAPI, client: TestClient) -> None:
    response = client.get(API_PATH + "/liveness")
    assert response.status_code == 200
