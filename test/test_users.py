from firebase_admin import auth
from fastapi.testclient import TestClient
from fixture import existing_user

from main import app
import uuid
import pytest

client = TestClient(app)

def test_get_users_success(auth_user):
    res = client.get("/users", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 200


def test_get_users_invalid_auth():
    res = client.get("/users")
    assert res.status_code == 401

def test_create_users_success(auth_user):
    res = client.post("/users", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    }, json={
        "username": "Louis",
        "email": "louis@gmail.com",
        "password": "louis"
    })
    assert res.status_code == 201

def test_create_users_invalid_auth():
    res = client.post("/users")
    assert res.status_code == 401

def test_get_users_by_id_success(auth_user, existing_user):
    user_id = existing_user['id']
    res = client.get(f"/users/{user_id}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 200
    assert res.json() == existing_user

def test_get_user_by_id_invalid_auth():
    user_id = uuid.uuid4()
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 401

def test_get_user_by_id_not_found(auth_user):
    user_id = str(uuid.uuid4())  
    res = client.get(f"/users/{user_id}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 404
