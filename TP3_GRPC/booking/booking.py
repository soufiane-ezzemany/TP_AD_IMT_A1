import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2_grpc
import showtime_pb2
import json


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.db:
            # Initialiser BookingData
            booking_data = booking_pb2.BookingData()
            booking_data.userid = booking["userid"]
            # Ajouter chaque reservation de l'utilisateur
            for date in booking["dates"]:
                date_obj = booking_data.dates.add()
                date_obj.date = date["date"]
                date_obj.movies.extend(date["movies"])

            # envoyer les données
            yield booking_data

    def GetBookingForUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                booking_data = booking_pb2.BookingData()
                booking_data.userid = booking["userid"]
                # Ajouter chaque reservation de l'utilisateur
                for date in booking["dates"]:
                    date_obj = booking_data.dates.add()
                    date_obj.date = date["date"]
                    date_obj.movies.extend(date["movies"])

                # envoyer les données
                return booking_data

        # Dans le cas ou il y a pas de reservations
        context.set_code(grpc.StatusCode.NOT_FOUND)
        return booking_pb2.BookingData()

    def AddBookingForUser(self, request, context):
        bookings = self.db
        userid = request.userid
        date = request.date
        movie = request.movieid

        # Calling grpc showtime service
        showtime = getShowtimeServiceData(date)

        if showtime is not None:
            movies = showtime.movies
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
                    # update the db
                    UpdateDb(bookings)
                    context.set_code(grpc.StatusCode.OK)
                    return booking_pb2.Response(response="Booking added successfully")

            context.set_code(grpc.StatusCode.CANCELLED)
            return booking_pb2.Response(response="Movie not found on this date")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return booking_pb2.Response(response="Couldn't add booking for the user")

# GRPC Showtime Service to get the movies for a specific date
def getShowtimeServiceData(date):
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)
        try:
            showtime = stub.GetMovieByDate(showtime_pb2.Date(date=date))
            return showtime
        except grpc.RpcError as e:
            return None

# Update the db
def UpdateDb(new_bookings):
    with open('{}/data/bookings.json'.format("."), "r") as rfile:
        bookings = json.load(rfile)
    # Update the bookings array
    bookings["bookings"] = new_bookings
    with open('{}/data/bookings.json'.format("."), "w") as wfile:
        json.dump(bookings, wfile, indent=2)
    wfile.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
