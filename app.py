from flask import Flask, request, jsonify,render_template
import requests
app = Flask(__name__)

@app.route('/save_location', methods=['GET','POST'])
def save_location():
    if request.method =="POST" :
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')
        print(data)
        print(lat)
        print(lon)
    return render_template("map.html")

if __name__ == '__main__':
    app.run(debug=True)
    