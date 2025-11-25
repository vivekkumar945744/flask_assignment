from flask import Flask, render_template, redirect, request, jsonify
import json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["flask_assignment"]
collection = db["form_data"]



@app.route("/api")
def api_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

@app.route("/", methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        try:
            collection.insert_one({"name": name, "email": email})
            return redirect('/success')
        except Exception as e:
            return render_template("form.html", error=str(e))
        
    return render_template("form.html")

@app.route('/success')
def success_page():
    return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=True)