from firebase_admin import auth
from fastapi.testclient import TestClient

from fixture import existing_fragment
from main import app
import uuid
import pytest

client = TestClient(app)

# Test get fragments with valid auth
def test_get_fragments_success(auth_user):
    res = client.get("/fragments", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 200

# Test get fragments with invalid auth
def test_get_fragments_invalid_auth():
    res = client.get("/fragments")
    assert res.status_code == 401

def test_create_fragment_success(auth_user):
    res = client.post("/fragments", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    }, json={
        "fragment": "moon",
        "price": "70€"
    })
    assert res.status_code == 201

# Test create fragment with invalid auth
def test_create_fragment_invalid_auth():
    res = client.post("/fragments")
    assert res.status_code == 401

# Test create fragment with invalid data (missing fragment)
def test_create_fragment_missing_fragment(auth_user):
    res = client.post("/fragments", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    }, json={
        "price": "70€"
    })
    assert res.status_code == 422

# Test create fragment with invalid data (missing price)
def test_create_fragment_missing_price(auth_user):
    res = client.post("/fragments", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    }, json={
        "fragment": "moon"
    })
    assert res.status_code == 422

# Test get fragment by ID with valid auth and existing fragment
def test_get_fragment_by_id_success(auth_user, existing_fragment):
    fragment_id = existing_fragment['id']
    res = client.get(f"/fragments/{fragment_id}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 200
    assert res.json() == existing_fragment


# Test get fragment by ID with invalid auth
def test_get_fragment_by_id_invalid_auth():
    fragment_id = uuid.uuid4()
    res = client.get(f"/fragments/{fragment_id}")
    assert res.status_code == 401

# Test get fragment by ID with non-existing fragment
def test_get_fragment_by_id_not_found(auth_user):
    fragment_id = str(uuid.uuid4())  # Generate a random fragment ID
    res = client.get(f"/fragments/{fragment_id}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}"
    })
    assert res.status_code == 404
