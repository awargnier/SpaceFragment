from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from classes.schema_dto import Fragment, FragmentNoID

from database.firebase import db
from routers.router_stripe import increment_stripe
from routers.router_auth import get_current_user

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
    increment_stripe(userData['uid'])
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
async def modify_fragment_name(fragment_id:str, modifiedFragment: FragmentNoID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('fragment').child(fragment_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        updatedFragment = Fragment(id=fragment_id, **modifiedFragment.model_dump())
        return db.child("users").child(userData['uid']).child('fragment').child(fragment_id).update(updatedFragment.model_dump(), userData['idToken'] )
    raise HTTPException(status_code= 404, detail="Fragment not found")

@router.delete('/{fragment_id}', status_code=204)
async def delete_fragment(fragment_id:str, userData: int = Depends(get_current_user)):
    try:
        fireBaseobject = db.child("users").child(userData['uid']).child('fragment').child(fragment_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403, detail="Unauthaurized"
        )
    if fireBaseobject is not None:
        return db.child("users").child(userData['uid']).child('fragment').child(fragment_id).remove(userData['idToken'])
    raise HTTPException(status_code= 404, detail="Session not found")

