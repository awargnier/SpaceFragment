from pydantic import BaseModel

# Model Pydantic = Datatype
class Fragment(BaseModel):
    id: str
    name: str

class FragmentNoID(BaseModel):
    name: str