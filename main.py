# Much of "main.py", "oauth2.py", and "user.py" are adapted from the OAuth2 
# tutorial at:
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# or if it is the distant future, here:
# https://web.archive.org/web/20230127160400/https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
#
# To run this you'll need to setup a postgres database and role that can 
# create tables. You can install FastAPI and other dependencies using pip.
#      pip install "fastapi[all]"
# You'll also need install uvicorn and run it with:
#      uvicorn main:app --reload
# then open index.html in a browser. 

from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db import get_user_from_db
from oauth2 import Token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user
from user import User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_user_from_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
