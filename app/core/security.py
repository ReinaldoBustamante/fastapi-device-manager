from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from .enums import RoleType
import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def create_token(data: dict):
    to_encode = data.copy()
    expire_in = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire_in})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def decode_token(token: str):
    token_decoded = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    return token_decoded

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        sub = payload.get('sub')
        email = payload.get('email')
        role_id = payload.get('role_id')
        if sub is None:
            raise credentials_exception
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

    return {
        "id": sub,
        "email": email,
        "role_id": role_id
    }

def require_admin(current_user = Depends(get_current_user)):
    if current_user['role_id'] != RoleType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user