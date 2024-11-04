import json
from bson import json_util, ObjectId

from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify
import os
import pprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi

#load .env file for MongoDB connection
load_dotenv()

app = Flask(__name__)

# Create a new client and connect to the server
client = MongoClient(os.environ.get("MONGODB_URI"), server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
#create database instance in our app
app.db = client.letsgo
#create flight collection if not exist otherwise use it
app.db.flight = app.db.flight

@app.route("/")
def home():
    flight_content = app.db.flight.find()
    return render_template("home.html", flights=flight_content)

@app.route("/flights", methods=["GET", "POST"])
def flight():
    flight_routes = []
    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        flight_capacity = request.form.get("flight_capacity")
        flight_origin = request.form.get("origin")
        flight_destination = request.form.get("destination")
        flight_routes.append({ "origin": flight_origin, "destination": flight_destination})
        new_flight = { "name": flight_number, "capacity": flight_capacity, "routes": flight_routes }
        flight_id = app.db.flight.insert_one(new_flight).inserted_id

       # return json.loads(json_util.dumps(flight_id))

    flights = app.db.flight.find()
    return render_template("flights.html", flights=flights)

app.run(debug=True)