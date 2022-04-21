from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from database.query import query_get, query_put, query_update
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from user import Auth
from user import AuthModel, UserModel, register_user, signin_user, update_user

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:19006"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
auth_handler = Auth()

@app.post('/signup')
def signup_api(user_details: UserModel):
    user = register_user(user_details)
    JSONResponse(status_code=200, content={'user': user})

@app.post('/signin')
def signin_api(user_details: AuthModel):
    user = signin_user(user_details.email, user_details.password)
    access_token = auth_handler.encode_token(user['email'])
    refresh_token = auth_handler.encode_refresh_token(user['email'])
    return JSONResponse(status_code=200, content={'token': {'access_token': access_token, 'refresh_token': refresh_token}, 'user': user})

@app.get('/refresh_token')
def refresh_token_api(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

@app.post("/user/update")
def update_user_api(user_details: UserModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        user = update_user(user_details)
        return JSONResponse(status_code=200, content={'user': user})
    return JSONResponse(status_code=401, content={'error': 'Faild to authorize'})

@app.get('/secret')
def secret_data_api(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@app.get('/notsecret')
def not_secret_data_api():
    return 'Not secret data'
