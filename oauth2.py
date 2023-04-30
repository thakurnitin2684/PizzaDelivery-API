from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import myToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return myToken.verify_token(data, credentials_exception)