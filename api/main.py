from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from database.query import query_get, query_put, query_update
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from auth import Auth
from user_model import AuthModel, UserModel

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
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
def signup(user_details: UserModel):
    user = query_get("SELECT * FROM user WHERE email = %s",(user_details.email))
    if len(user) != 0:
        print(user)
        return 'Account already exists'
    hashed_password = auth_handler.encode_password(user_details.password)
    user = query_put("""
                INSERT INTO user (
                    first_name,
                    last_name,
                    email,
                    password_hash
                ) VALUES (%s,%s,%s,%s)
                """,
                (
                    user_details.first_name,
                    user_details.last_name,
                    user_details.email,
                    hashed_password
                )
    )
    print(user)
    return user

@app.post('/signin')
def signin(user_details: AuthModel):
    user = query_get("SELECT * FROM user WHERE email = %s",(user_details.email))
    if len(user) == 0:
        print('Invalid email')
        raise HTTPException(status_code=401, detail='Invalid email')
    if (not auth_handler.verify_password(user_details.password, user[0]['password_hash'])):
        print('Invalid password')
        raise HTTPException(status_code=401, detail='Invalid password')
    
    access_token = auth_handler.encode_token(user[0]['email'])
    refresh_token = auth_handler.encode_refresh_token(user[0]['email'])
    return JSONResponse(status_code=200, content={'token': {'access_token': access_token, 'refresh_token': refresh_token}, 'user': user[0]})

@app.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

@app.post("/user/update")
def update_user(user_details: UserModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        hashed_password = auth_handler.encode_password(user_details.password)
        query_put("""
            UPDATE user 
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password_hash = %s 
                WHERE user.email = %s;
            """,
            (
                user_details.first_name,
                user_details.last_name,
                user_details.email,
                hashed_password,
                user_details.email,
            )
        )
        user = query_get("SELECT * FROM user WHERE email = %s",(user_details.email))
        return JSONResponse(status_code=200, content={'user': user[0]})
    return JSONResponse(status_code=401, content={'error': 'Faild to authorize'})

@app.get('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@app.get('/notsecret')
def not_secret_data():
    return 'Not secret data'
