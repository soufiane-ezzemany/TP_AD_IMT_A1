from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
import grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)


PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/user/<userId>", methods = ['GET'])
def get_user_by_id(userId):
   for user in users:
      if str(user["id"]) == str(userId):
         res = make_response(jsonify(user), 200)
         return res
   return make_response(jsonify({"error": "No user with this ID"}), 400)


@app.route("/user/<userId>/reservations", methods=['GET'])
def get_user_reservations_by_id(userId):

   bookingsReq = getBookingServiceData(userId)

   if bookingsReq is not None:
      bookings = bookingsReq
      for reservation in bookings["dates"]:
         reservation["movieData"] = []
         for movie in reservation["movies"]:
            query = f'''
            {{
                movie_with_id(_id: "{movie}") {{
                  id,title,director,rating
                }}
            }}
            '''
            moviesReq = requests.post(f"http://{request.remote_addr}:3200/graphql",json={'query': query}) # GraphQL
            if moviesReq.status_code == 200:
               movieData = moviesReq.json()
               reservation["movieData"].append(movieData)
            else:
               return make_response(jsonify({"error": "No movies found"}), 400)

      return bookings
   else:
      return make_response(jsonify({"error": "No bookings found for this user"}), 400)


# GRPC Booking Service to get the reservations for a specific user
def getBookingServiceData(user):
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        try:
            bookings = stub.GetBookingForUser(booking_pb2.UserID(userid=user))
            return json_transform(bookings)
        except grpc.RpcError as e:
            return None

def json_transform(input_object):
   # Initialize the result dictionary
   result = {"userid": input_object.userid, "dates": []}
   print(input_object.dates)
   # Iterate over the dates
   for date_entry in input_object.dates:
      # Each date entry is converted to a dictionary
      date_dict = {
         "date": date_entry.date,
         "movies": list(date_entry.movies)
      }
      result['dates'].append(date_dict)

   return result


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
