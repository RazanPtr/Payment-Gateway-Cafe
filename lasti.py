from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from typing import List
from pymongo import MongoClient

client = MongoClient("mongodb+srv://lasti:123@cluster0.pyp54fo.mongodb.net/?retryWrites=true&w=majority")
db = client['cafe']
collection = db['payment']

data = collection.find_one()

def write_data(data):
    collection.replace_one({}, data, upsert=True)

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
app = FastAPI()
JWT_SECRET = 'myjwtsecret'
ALGORITHM = 'HS256'

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
authentication = APIRouter(tags=["Authentication"])

def get_user_by_username(username):
    for desain_user in data['user']:
        if desain_user['username'] == username:
            return desain_user
    return None

def authenticate_user(username: str, password: str):
    user_data = get_user_by_username(username)
    if not user_data:
        return None

    user = User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])

    if not user.verify_password(password):
        return None

    return user

@authentication.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        print(f"Invalid username or password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    token = jwt.encode({'id': user.id, 'username': user.username}, JWT_SECRET, algorithm=ALGORITHM)

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = get_user_by_username(payload.get('username'))
        return User(id=user['id'], username=user['username'], password_hash=user['password_hash'])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

@authentication.post('/users')
async def create_user(username: str = Form(...), password: str = Form(...)):
    last_user_id = data['user'][-1]['id'] if data['user'] else 0
    user_id = last_user_id + 1
    user = User(id=user_id, username=username, password_hash=bcrypt.hash(password))
    data['user'].append(jsonable_encoder(user))
    write_data(data)
    return {'message': 'User created successfully'}

@authentication.post('/payment')
async def add_payment(
    fullname: str = Form(...),
    nameoncard: str = Form(...),
    emailaddress: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    daybirth: str = Form(...),
    monthbirth: str = Form(...),
    yearbirth: str = Form(...),
    gender: str = Form(...),
    payment: str = Form(...),
    cardnumber: str = Form(...),
    cardcvv: str = Form(...),
    expmonth: str = Form(...),
    expyear: str = Form(...),
    amount: str = Form(...)
):
    # increment id otomatis
    last_user_id = data['payment'][-1]['id_payment'] if data['payment'] else 0
    user_id = last_user_id + 1

    # Menambahkan data ke masing-masing tabel
    data['payment'].append({
        "id_payment": user_id,
        "fullname": fullname,
        "nameoncard": nameoncard,
        "emailaddress": emailaddress,
        "address": address,
        "city": city,
        "daybirth": daybirth,
        "monthbirth": monthbirth,
        "yearbirth": yearbirth,
        "gender": gender,
        "payment": payment,
        "cardnumber": cardnumber,
        "cardcvv": cardcvv,
        "expmonth": expmonth,
        "expyear": expyear,
        "amount": amount
    })

    # Menyimpan data ke file
    write_data(data)

    return "Add data successfully"

app.include_router(authentication)