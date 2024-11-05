import json
from bson import json_util, ObjectId

from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, flash, url_for, jsonify
import os
import pprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flight import Flight

#load .env file for MongoDB connection
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET")

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
    flight_details = Flight()
    if request.method == "POST":

        flight_details = Flight(request.form)

        flight_number = flight_details.flight_number.data
        flight_capacity = flight_details.flight_capacity.data
        flight_origin = flight_details.flight_origin.data
        flight_destination = flight_details.flight_destination.data

        flight_routes.append({ "origin": flight_origin, "destination": flight_destination})
        new_flight = { "name": flight_number, "capacity": flight_capacity, "routes": flight_routes }
        flight_id = app.db.flight.insert_one(new_flight).inserted_id
        flash("Successfully Inserted!", "success")
       # return json.loads(json_util.dumps(flight_id))

    if request.method == "UPDATE":
        pass
    flights = app.db.flight.find()
    return render_template("flights.html", form=flight_details, flights=flights)

app.run(debug=True)