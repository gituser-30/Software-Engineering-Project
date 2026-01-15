from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models import Register, Login
from utils import generate_otp, send_email_otp, hash_password, verify_password
from database import users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=True,
    allow_methods=["*"],   # allow all methods (GET, POST, OPTIONS)
    allow_headers=["*"],   # allow all headers
)
otp_store = {}

@app.post("/register/send-otp")
def send_otp_route(data: Register):
    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    otp = generate_otp()
    otp_store[data.email] = {"otp": otp, "data": data}
    send_email_otp(data.email, otp)
    return {"message": "OTP sent to email"}

@app.post("/register/verify-otp/{email}/{otp}")
def verify_otp(email: str, otp: int):
    if email not in otp_store or otp_store[email]["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    data = otp_store[email]["data"]
    users.insert_one({
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password)
    })
    del otp_store[email]
    return {"message": "Registration successful"}

@app.post("/login")
def login(data: Login):
    user = users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Login successful", "user": {"name": user["name"], "email": user["email"]}}
