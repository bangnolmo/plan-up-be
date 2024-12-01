import sys
import os

#시스템 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post("/login", json={"user_id": "test@test.com", "ac_token": "ac_test", "re_token": "re_test"})
    assert response.status_code == 200
    print(response.json())

def test_create_time_table():
    response = client.post("/timeTable", json={"name": "test", "year": 2021, "semester": 1, "owner": "testUser"})
    assert response.status_code == 200
    print(response.json())

def test_get_time_table():
    response = client.get("/timeTable?email=test@test.com")
    assert response.status_code == 200
    print(response.json())

def test_get_time_table_lectures():
    response = client.get("/timeTable/lectures/1")
    assert response.status_code == 200
    print(response.json())

def test_insert_time_table_lectures():
    response = client.post("/timeTable/lectures/insert", json={"table_idx": 1, "class_idx": 12024201, "sub_num": 102030})
    # assert response.status_code == 200
    print(response.json(), response.status_code)

if __name__ == "__main__":
    test_login()
    test_create_time_table()
    test_get_time_table()
    test_get_time_table_lectures()
    test_insert_time_table_lectures()