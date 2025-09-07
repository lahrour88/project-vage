from flask import Flask, render_template, request, redirect, url_for,session ,send_from_directory,Response
from dotenv import load_dotenv
from data import data
load_dotenv()
import time
import requests
import os
from vage import send_email ,user
from delay import get_data ,data_in_table_,data_analise_
app = Flask(__name__)
app.secret_key=os.getenv("session_key")
url=os.getenv("url")
api_key =os.getenv("api_key")
from datetime import timedelta

app.permanent_session_lifetime = timedelta(days=7)  # Ù…Ø¯Ø© Ø¨Ù‚Ø§Ø¡ Ø§Ù„Ø¬Ù„Ø³Ø©




@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(os.path.dirname(__file__), 'service-worker.js')


#  robots.txt
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt", mimetype="text/plain")

#  sitemap.xml
@app.route("/sitemap.xml")
def sitemap():
    with open("static/sitemap.xml", "r", encoding="utf-8") as f:
        sitemap_xml = f.read()
    return Response(sitemap_xml, mimetype="application/xml")


    
    
@app.route("/work",methods=["get","post"])
def work():
    return render_template("work.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error=""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,"and",password)
        # Ù‡Ù†Ø§ ØªØ¶Ø¹ Ù…Ù†Ø·Ù‚ Ø§Ù„ØªØ­Ù‚Ù‚ Ù…Ù† ØµØ­Ø© Ø§Ù„Ø¨ÙŠØ§Ù†Ø§Øª
        if username == 'admin' and password == 'admin123':  # Ù‡Ø°Ø§ Ù…Ø«Ø§Ù„ ÙÙ‚Ø·ØŒ Ø§Ø³ØªØ®Ø¯Ù… Ù‚Ø§Ø¹Ø¯Ø© Ø¨ÙŠØ§Ù†Ø§Øª ÙÙŠ Ø§Ù„ØªØ·Ø¨ÙŠÙ‚ Ø§Ù„Ø­Ù‚ÙŠÙ‚ÙŠ
            session['logged_in'] = True
            session['username'] = username
            session.permanent = True
            print(session)
            return redirect(url_for('admin_page'))
        else:
            error="Ø®Ø·Ø£ ÙÙŠ Ø§Ø³Ù… Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù… Ø§Ùˆ ÙƒÙ„Ù…Ø© Ø§Ù„Ù…Ø±ÙˆØ±"
    return render_template('login.html',error=error)
    
@app.route("/admin")
def admin_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        get_data()
        return render_template("admin.html",table_data=data_in_table_,chart_data=data_analise_)
# 1 page price img text to add_data()
@app.route("/",methods=["GET","POST"])
def home():
    if request.method== "POST":
        value=request.form.get('type')
        if not value :
            print(value)
            message="Ø§Ù„Ù…Ø±Ø¬Ùˆ Ù…Ù†Ùƒ Ù…Ù„Ø£ Ø§Ø­Ø¯ Ø§Ù„Ø®ÙŠØ§Ø±Ø§Øª "
            return render_template("home.html",message=message)
        else:
            index=int(value)
            price=data[index]["price"]
            vage_info=data[index]["vage_info"]
            img=data[index]["img"]
            print(img)
            vage_type=data[index]["vage_type"]
            #session 
            session["img"]=img
            session["vage_type"]=vage_type
            return redirect(url_for('add_data',img=img,vage_info=vage_info,price=price))
    return render_template("home.html")
        
#add_data page get data from form and home()
@app.route("/add", methods=["GET", "POST"])
def add_data():
    try:
        result="    "
        vage_info=request.args.get("vage_info")
        price=request.args.get("price")
        img=request.args.get("img")
        print("img in add_data is :",img)
        if request.method == "POST":
        #user data 
            vage_type=session.get("vage_type")
            img=session.get("img")
            full_name = request.form["user_name"]
            email = request.form["email"]
            phone_number= request.form["phone_number"]
            adresse =request.form.get("adresse")
        #car data
            car_category=request.form["car_category"]
            car_model=request.form.get("modul_car")
            appointment_date=request.form["day"]
            appointment_time = request.form["minut"]
            user_data = user(full_name, email, phone_number, car_model, car_category, appointment_date, appointment_time,vage_type,adresse)
            data = {
            "appointment_date":user_data.appointment_date,
            "appointment_time":user_data.appointment_time,
            "full_name": user_data.full_name,
            "email": user_data.email,
            "phone_number": user_data.phone_number,
            "car_category":user_data.car_category,
            "car_model":user_data.car_model,
            "vage_type":user_data.vage_type,
            "adresse":user_data.adresse
            }
            print(f'data :\n {data}')
            headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
            }
        #conect supabase with requests
            response = requests.post(url, headers=headers,json=data)
            result="Ù„Ù‚Ø¯ ØªÙ… Ø­Ø¬Ø² Ø§Ù„Ù…ÙˆØ¹Ø¯ Ø¨Ù†Ø¬Ø§Ø­"
            print(response.json(),"\n")
            print(session)
    except Exception as e :
        print(e)
        result="ÙØ´Ù„ Ø¹Ù…Ù„ÙŠØ© Ø§Ù„Ø­Ø¬Ø² Ø§Øا¹Ø¯ ØªÙ„Ù…Ø­Ø§ÙˆÙ„Ø© Ù„Ø§Ø­Ù‚Ø§"
    return render_template("add.html",price=price,vage_info=vage_info,img=img,result=result)
    
@app.route("/about",methods=["GET","POST"])
def about():
    if request.method=="POST":
        user_name=request.form["user_name"]
        phone_number =request.form["phone_number"]
        email=request.form["email"]
        message=request.form["message"]
        body=f"hello my name is {user_name}\n my phone number :{phone_number}\n oky \n :{message}"
        send_email(email,body)
    return render_template("about.html")
if __name__ == "__main__":
    app.run(port=5000,debug=False)
