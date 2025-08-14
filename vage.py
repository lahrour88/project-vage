import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
class user:
    def __init__(self,full_name, email, phone_number,car_model,car_category,appointment_date,appointment_time,vage_type,adresse):
        self.full_name = full_name
        self.email= email
        self.phone_number= phone_number
        self.car_category=car_category
        self.car_model=car_model
        self.appointment_date=appointment_date
        self.appointment_time=appointment_time
        self.vage_type=vage_type
        self.adresse=adresse
        

from_email=os.getenv("email")
password=os.getenv("password")
def send_email(email,body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "email from python"
    msg['From'] = from_email
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)
