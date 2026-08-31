from jose import jwt,JWTError
from datetime import datetime ,timedelta,timezone

from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="login")

# tokrn create 
def create_token (data : dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def verify_token (token :str = Depends(oauth2_schemas)):
    try:
        payload  = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException (status_code=401,detail="invalid user")


