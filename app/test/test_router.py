import sys
import os

# 시스템 경로 추가
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def headers():
    return {"Authorization": "Bearer test_token"}


def setup_module():
    """공통 데이터 준비"""
    client.post(
        "/timeTable",
        json={"name": "test", "year": 2021, "semester": 1, "owner": "test@test.com"},
    )


def teardown_module():
    """공통 데이터 정리"""
    client.delete("/timeTable", params={"table_idx": 1})


def test_login():
    response = client.post(
        "/login",
        json={"user_id": "test@test.com", "ac_token": "ac_test", "re_token": "re_test"},
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Login Successful"


def test_create_time_table(headers):
    response = client.post(
        "/timeTable",
        json={"name": "test", "year": 2021, "semester": 1, "owner": "test@test.com"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json().get("message") == "TimeTable Created"


def test_get_time_table(headers):
    response = client.get("/timeTable?email=test@test.com", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "name" in data[0]
    assert data[0]["name"] == "test"


def test_put_time_table_lectures(headers):
    response = client.put(
        "/timeTable/lectures",
        json={"table_idx": 1, "class_idx": 12024201, "sub_num": "004"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == "TimeTable Lecture Inserted Successfully"


def test_get_time_table_lectures(headers):
    response = client.get("/timeTable/lectures/1", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_time_table(headers):
    response = client.delete("/timeTable", params={"table_idx": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json() == "TimeTable Deleted Successfully"


def test_delete_time_table_lectures(headers):
    response = client.delete(
        "/timeTable/lectures", params={"table_idx": 1, "class_idx": 1}, headers=headers
    )
    assert response.status_code == 200
    assert response.json() == "TimeTable Lecture Deleted Successfully"
