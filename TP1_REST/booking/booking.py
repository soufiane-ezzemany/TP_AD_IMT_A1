from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1>Welcome to the booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"Booking for user not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   req = request.get_json()
   date = req['date']
   movie = req['movieid']
   # create the url
   url = f"http://{request.remote_addr}:3202/showtimes/{date}"
   # get the showtimes information
   showtimes = requests.get(url)
   # check if the date exists
   if showtimes.status_code == 200:
       showtime_movies = showtimes.json()
       movies = showtime_movies['movies']
       for _movie in movies:
           if movie == _movie:
              user_entry = next((entry for entry in bookings if entry["userid"] == userid), None)
              if user_entry is None:
                  # User doesn't exist, create a new entry
                  user_entry = {"userid": userid, "dates": []}
                  bookings.append(user_entry)
                  user_entry["dates"].append({"date": date, "movies": [movie]})
              else:
                  date_entry = next((entry for entry in user_entry["dates"] if entry["date"] == date), None)
                  if date_entry is None:
                      date_entry = {"date": date, "movies": [movie]}
                      user_entry["dates"].append(date_entry)
                  else:
                      date_entry["movies"].append(movie)

              return make_response(jsonify({"ok": "booking added"}), 200)

       return make_response(jsonify({"error": "Movie not found on this date"}), 400)
   else:
       return make_response(jsonify({"error": "Couldn't add booking for the user"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
