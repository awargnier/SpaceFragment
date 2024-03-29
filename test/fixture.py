import uuid

from classes.schema_dto import Fragment, User
from database.firebase import db
import pytest

@pytest.fixture
def existing_fragment():
    # Create a fake fragment with an ID
    existing_fragment_id = str(uuid.uuid4())
    existing_fragment = Fragment(id=existing_fragment_id, fragment="Moon", price="70€")

    # Save the fragment to the Firebase database
    db.child("fragments").child(existing_fragment_id).set(existing_fragment.model_dump())

    return existing_fragment

@pytest.fixture
def existing_user():
    existing_user_id = str(uuid.uuid4())
    existing_user = User(id=existing_user_id, username="Jean", email="jean@gmail.com", password="Jean")

    db.child("users").child(existing_user_id).set(existing_user.model_dump())

    return existing_user