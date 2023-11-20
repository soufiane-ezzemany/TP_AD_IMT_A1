# UE DISTRIBUTED ARCHITECTURE : MIX - GraphQl

## Project Overview
This project focused on building microservices using Flask. In this project, we implement the movie service using GraphQl.

![ARCHITECTURE](https://helene-coullon.fr/images/graphql.png)

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
    cd TP2_GRAPHQL
    pip install -r requirements.txt
    # Or use Pycharm that will auto install the requirements
    ```

3. **Launch the movie service:**
     ```bash
    cd movie
    python movie.py
    ```
   The playground is avaible on http://127.0.0.1:3200/graphql

Now you're ready to explore and run the project!
