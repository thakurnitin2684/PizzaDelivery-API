from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal,engine
from schemas import SignUpModel,LoginModel
from models import User
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
import myToken
import oauth2

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']

)


session=SessionLocal(bind=engine)

@auth_router.get('/')
async def hello(current_order: User = Depends(oauth2.get_current_user)):
    """
        ## Sample hello world route for auth route
    
    """
    return {"message":"Hello World!, auth"}


@auth_router.post('/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(user:SignUpModel):
    """
        ## Create a user
        This requires the following
        ```
                username:int
                email:str
                password:str
                is_staff:bool
                is_active:bool

        ```
    
    """


    db_email=session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    db_username=session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)

    session.commit()
    session.refresh(new_user)
    return new_user



#login route

@auth_router.post('/login',status_code=200)
async def login(request:OAuth2PasswordRequestForm = Depends()):
    """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns a token pair `access` and `refresh`
    """
    db_user=session.query(User).filter(User.username==request.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not check_password_hash(db_user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = myToken.create_access_token(data={"sub": db_user.username})
    response= {"access_token": access_token, "token_type": "bearer"}

    return response

