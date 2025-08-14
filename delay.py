from flask import Flask, render_template
import time ,os
from dotenv import load_dotenv
from data import data
url=os.getenv("url")
api_key =os.getenv("api_key")
data_in_table_ = []
data_analise_ = []
import requests
# ----------------- دوال المساعدة -----------------

def data_in_table(user):
    data_in_table_.append(user)

def data_analise(user):
    data_analise_.append(user)

def delete_data(user_id):
    delete_url = f"{url}?id=eq.{user_id}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.delete(delete_url, headers=headers)
    print(f"Deleted {user_id}, Status:", response.status_code)

# ----------------- جلب البيانات -----------------

def get_data():
    data_in_table_.clear()
    data_analise_.clear()

    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data = data[::-1]  # ترتيب عكسي

    ONE_WEEK = 60*60*2
    THREE_MONTHS = 90 * 24 * 60 * 60

    for user in data:
        user_id = user["id"]
        appointment_datetime = f"{user['appointment_date']} {user['appointment_time']}"
        t = time.strptime(appointment_datetime, "%Y-%m-%d %H:%M:%S")
        appointment_seconds = int(time.mktime(t))
        current_time = time.time()

        one_week_after = appointment_seconds + ONE_WEEK
        three_months_after = appointment_seconds + THREE_MONTHS

        if current_time < one_week_after:
            data_in_table(user)
        elif one_week_after <= current_time < three_months_after:
            data_analise(user)
        else:
            delete_data(user_id)

# -----------------
