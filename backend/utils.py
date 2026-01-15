import random
from passlib.context import CryptContext
import smtplib
from email.message import EmailMessage

EMAIL = "Email User"
PASSWORD = "Email Password"  # Add your app password here

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)
# def hash_password(password):
#     return pwd_context.hash(password.encode('utf-8')[:72])


# def verify_password(password, hashed):
#     return pwd_context.verify(password.encode('utf-8'), hashed)


def generate_otp():
    return random.randint(100000, 999999)

def send_email_otp(receiver_email, otp):
    email = EmailMessage()
    email["Subject"] = "Your OTP Verification Code"
    email["From"] = EMAIL
    email["To"] = receiver_email
    email.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(email)
