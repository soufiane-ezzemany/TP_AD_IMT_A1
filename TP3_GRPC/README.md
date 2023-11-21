# UE DISTRIBUTED ARCHITECTURE : MIX - GRPC

## Project Overview
This project focused on building microservices using Flask. In this project, we implement the showtime and booking service in GRPC.

[![img.jpg](https://i.postimg.cc/Kjm0W4j7/img.jpg)](https://postimg.cc/ftg7tzxk)

## Services
### User
This service handles operations related to users, such as creating and managing user bookings.
### Booking
This service allows retrieving the list of all reservations, consulting reservations associated with a specific user.
### Movie
This service allows retrieving movie by title or identifier, updating movie rating or title, adding new movies to the database and deleting a movie.
### Showtime
This service provides the functionality to display a list of all movies along with their screening schedules and allows filtering movies shown on a specific date.
## Getting Started

To get started with the project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/soufiane-ezzemany/TP_AD_IMT_A1.git
    ```

2. **Install the required dependencies:**

    ```bash
    cd TP2_GRPC
    pip install -r requirements.txt
    # Or use Pycharm that will auto install the requirements
    ```

3. **Launch the movie service:**
     ```bash
    cd movie
    python movie.py
    ```
   The playground is avaible on http://127.0.0.1:3200/graphql

4. **Launch the booking service:**
     ```bash
    cd booking
    python booking.py
    ```
5. **Launch the showtime service:**
     ```bash
    cd showtime
    python showtime.py
    ```
**Note:** The files containing the stub, servicer and the marshalling/inmarshalling are already generated and avaible.
But if you to regenerate them after a modification on the proto file : 
    ```
  python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. your_proto_file.proto
    ```

Now you're ready to explore and run the project!
