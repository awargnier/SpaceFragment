from pydantic import BaseModel
import uuid

# Model Pydantic = Datatype
class Fragment(BaseModel):
    id: str
    name: str

class FragmentNoID(BaseModel):
    name: str

class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str

class UserNoID(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str