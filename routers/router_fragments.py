from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from classes.schema_dto import Fragment, FragmentNoID

from database.firebase import db

router= APIRouter(
    prefix='/fragments',
    tags=["Fragments"]
)

fragment = [
    Fragment(id="s1", name="Moon"),
    Fragment(id="s2", name="Mars"),
    Fragment(id="s3", name="Meteorite")
]


@router.get('/', response_model=List[Fragment])
async def get_fragment():
    fireBaseObject = db.child('fragment').get().val()
    resultArray = [value for value in fireBaseObject.values()]
    return resultArray

@router.post('/', response_model=Fragment, status_code=201)
async def create_fragment(givenName:FragmentNoID):
    generatedId=uuid.uuid4()
    newFragment= Fragment(id=str(generatedId), name=givenName)
    # fragment.append(newFragment)
    db.child("fragment").child(str(generatedId)).set(newFragment.model_dump())
    return newFragment

@router.get('/{fragment_id}', response_model=Fragment)
async def get_fragment_by_ID(fragment_id:str): 
    for fragment in fragments:
        if fragment.id == fragment_id:
            return fragment
    raise HTTPException(status_code= 404, detail="Fragment not found")

@router.patch('/{fragment_id}', status_code=204)
async def modify_fragment_name(fragment_id:str, modifiedFragment: FragmentNoID):
    for fragment in fragments:
        if fragment.id == fragment_id:
            fragment.name=modifiedFragment.name
            return
    raise HTTPException(status_code= 404, detail="Fragment not found")

@router.delete('/{fragment_id}', status_code=204)
async def delete_fragment(fragment_id:str):
    for fragment in fragments:
        if fragment.id == fragment_id:
            fragment.remove(fragment)
            return
    raise HTTPException(status_code= 404, detail="Fragment not found")