from fastapi import APIRouter, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from classes.schema_dto import UserAuth
from firebase_admin import auth
from database.firebase import authUser

router= APIRouter(
    prefix='/auth',
    tags=["Auth"]
)


@router.post('/signup', status_code=201)
async def create_an_account(userAuth_body: UserAuth):
    try:
        userAuth = auth.create_user(
            email = userAuth_body.email,
            password = userAuth_body.password
        )
        return {
            "message": f"Nouvel utilisateur créé avec id : {userAuth.uid}"
        }
    except auth.EmailAlreadyExistsError: 
        raise HTTPException(
            status_code = 409,
            detail = f"Un compte existe déja pour cet email : {userAuth_body.email}"
        )

#Login endpoint
@router.post('/login')
async def create_swagger_token(user_credentials:OAuth2PasswordRequestForm = Depends()):
    try:
        print(user_credentials)
        user = authUser.sign_in_with_email_and_password(email=user_credentials.username, password=user_credentials.password)
        token = user['idToken']
        print(token)
        return {
            "access_token" : token,
            "token_type" : "bearer"
        }
    except:
        raise HTTPException(
            status_code=401,
            details="Invalid credentials"
        )
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(provided_token: str = Depends(Oauth2_scheme)):
    decoded_token = auth.verify_id_token(provided_token)
    decoded_token['idToken'] = provided_token
    return decoded_token

#Proteger la route pour recuperer les data perso
@router.get('/me')
def secure_endpoint(userData: int = Depends(get_current_user)):
    return userData
