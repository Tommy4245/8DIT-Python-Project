import requests #Imports the requests package, this allows me to make my API calls
import sys #Imports sys, this allows me to use the function sys.exit() 
import os  #Imports os so I am able to check if a user has PIP and reuests installed 
import config #This is imported from another local file and contains my API Key

try:
    import requests
except ImportError:
    print("Please install the requests package by running")
    print("pip install requests")
    print("This program can not run without the requests package")
    print("Exiting...")
    os._exit(1)

watchlist_to_make_instances = []

class MovieAPI:
    """Class to interact with the Movie Database API being TMDb"""

    def __init__(self, user_url_input):
        """Initialize MovieAPI object by useing __init__ with base URL and API key from config.py"""
        self.base_url = "https://api.themoviedb.org"
        self.user_url_input = user_url_input
        self.api_key = config.API_KEY

    def get_movie_info(self):
        """This Function makes a endpoint and then Fetches key infomation from the TMDb API"""
        endpoint = self.base_url + self.user_url_input + f"&api_key={self.api_key}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print("API call failed")
            return None


class UsersWatchlist:
    """Class which allows the user to manage and modify movies in there watchlist"""
    
    def __init__(self):
        """Initalizes the Object by useing __init__ and makeing a empty list for the users watchlist"""
        self.watchlist_list = []

    def add_movies_to_watchlist(self, movie_title, movie_rating, movie_genre, movie_overview):
        """Makes all the instances of data the User needs for the Watchlist then appends it to the empty list"""
        self.watchlist_list.append([movie_title, movie_rating, movie_genre, movie_overview])

    def watchlist(self):
        """This Function displays the Users Watchlist by printing out the self.watchlist_list, it also allows for the user to modify the list"""
        length_of_watchlist = len(self.watchlist_list)
        if length_of_watchlist == 0:
            print("Currently there are no movies in your watchlist")
            print("Returning to Menu")
            menu()
        else:
            for watch, movie_info in enumerate(self.watchlist_list):
                print("\nID Number:", watch + 1)
                print("Title:", movie_info[0])
                print("Rating:", movie_info[1])
                print("Genre:", movie_info[2])
                print("Overview:", movie_info[3])
        menu_or_remove = string_input_validation("Please type Remove to remove items from your watchlist, if you do not want to do this please type Menu to return to the menu", "REMOVE", "MENU", "Please Choose a Valid Option which is Remove or Menu")
        if menu_or_remove == "MENU":
            print("Now returning to the Menu")
            menu()
        elif menu_or_remove == "REMOVE":
            self.remove_movies_from_watchlist()

    def remove_movies_from_watchlist(self):
        """Allows for the user to remove items from there watchlist"""
        remove_movie_number = number_input_validation("Looking at the Movie ID Number please enter the Movie ID Number of the Movie you would like to remove", 1, len(self.watchlist_list))
        if remove_movie_number == 0:
            menu()
        else:
            del watchlist_to_make_instances[remove_movie_number - 1]
        print("Your New Watchlist is\n")
        getting_watchlist_to_object()
        remove_something_else = string_input_validation("Would you like to Remove anything else, please type 'yes' or 'no'", "YES", "NO", "Please Choose a Valid Option which is Yes or No")
        if remove_something_else == "YES":
            getting_watchlist_to_object()
            self.remove_movies_from_watchlist()
        elif remove_something_else == "NO":
            print("Returning to menu")
            menu()


def number_input_validation(msg, minimum, maximum):
    """Validate int values that the user has selected and has boundarys to validate the user response is in range, also allows the user to return to the menu at any time if they type 0"""
    print(msg)
    while True:
        try:
            user_response = int(input(":"))
            if user_response == 0:
                menu()
            elif minimum <= user_response <= maximum:
                return user_response
            else:
                print("That item is not in range")
        except ValueError:
            print("Invalid answer")

def string_input_validation(msg, option1, option2, invalid_select_option1_or_2):
    """Validate string input againts options by haveing 2 valid awnsers, also allows the user to return to the menu at any time if they type 0"""
    print(msg)
    while True:
        try:
            users_choice = input(":")
            if users_choice == "0":
                menu()
            users_choice = users_choice.upper()
            if users_choice == option1 or users_choice == option2:
                return users_choice
            else:
                print(invalid_select_option1_or_2)
        except:
            print(invalid_select_option1_or_2)

def getting_watchlist_to_object():
    """Convert watchlist data into UsersWatchlist object by useing the external list watchlist_to_make_instances"""
    watchlist_version = UsersWatchlist() 
    for watch in range(len(watchlist_to_make_instances)): 
        title = watchlist_to_make_instances[watch][0]
        rating = watchlist_to_make_instances[watch][1]
        genre = watchlist_to_make_instances[watch][2]
        overview = watchlist_to_make_instances[watch][3]
        watchlist_version.add_movies_to_watchlist(title, rating, genre, overview)  
    watchlist_version.watchlist()


def movie_appending_and_printing_system(movie_data):
    """Append movie data to the watchlist_to_make_instances external list and prints data from the API so a User can decide what movies they want to add to there watchlist"""
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {"accept": "application/json", "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YmQ3YzJjNTg0ZmIwMzA2NWFmMjQ1YjY4NGQxNWFkMSIsInN1YiI6IjY2MDRkMGU3MTVkZWEwMDE4NTI3NmU0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URJ1s8L_2rhk4quhJbuXHzajszCJN58mpX1u1vvP8uU"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        genre_dict = response.json()
        genre_names = {genre['id']: genre['name'] for genre in genre_dict.get('genres', [])}
    else:
        print("Failed to fetch genre data")
        return
    if movie_data:
        movie_info_list = []
        for id_number, movie in enumerate(movie_data['results']):
            movie_info = []
            genres = [genre_names.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])]
            genres_str = ', '.join(genres)
            movie_info.append(movie['title'])
            movie_info.append(movie['vote_average'])
            movie_info.append(genres_str)
            movie_info.append(movie['overview'])
            movie_info_list.append(movie_info)
            print(f"ID Number: {id_number + 1}")
            print(f"Title: {movie['title']}")
            print(f"Rating: {movie['vote_average']}")
            print(f"Genres: {genres_str}")
            print(f"Overview: {movie['overview']}")
            print()
        the_movie_user_wants = number_input_validation("Looking at the ID numbers above, would you like to add a Movie to your watchlist? Rember to type 0 if you would not like to so you can return to the menu", 1, len(movie_data['results']))
        watchlist_to_make_instances.append(movie_info_list[the_movie_user_wants - 1])
        menu()


def year_movie_filter():
    """Filters Movies by there release Year, I have given the user the option to select Movies from 2000 - 2024"""
    movie_year = number_input_validation("What years Movies do you want to filter through, I offer from 2000 - 2024", 2000, 2024)
    api_url_user_request = f"/3/discover/movie?primary_release_year={movie_year}"
    movie_api = MovieAPI(api_url_user_request)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)


def genre_movie_filter():
    """Filters Movies by Genre"""
    genre_ids = [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37]
    print("Please Type 1 to Filter for Action")
    print("Please Type 2 to Filter for Adventure")
    print("Please Type 3 to Filter for Animation")
    print("Please Type 4 to Filter for Comedy")
    print("Please Type 5 to Filter for Crime")
    print("Please Type 6 to Filter for Documentry")
    print("Please Type 7 to Filter for Drama")
    print("Please Type 8 to Filter for Family")
    print("Please Type 9 to Filter for Fantasy")
    print("Please Type 10 to Filter for History")
    print("Please Type 11 to Filter for Horror")
    print("Please Type 12 to Filter for Music")
    print("Please Type 13 to Filter for Mystery")
    print("Please Type 14 to Filter for Romance")
    print("Please Type 15 to Filter for Science Fiction")
    print("Please Type 16 to Filter for TV Movie")
    print("Please Type 17 to Filter for Thriller")
    print("Please Type 18 to Filter for War")
    print("Please Type 19 to Filter for Western")
    movie_genre = number_input_validation("Please choose a Genre you would like to filter with",1, 19)
    movie_genre = movie_genre - 1
    users_chosen_genre = genre_ids[movie_genre]
    api_url_user_request = f"/3/discover/movie?with_genres={users_chosen_genre}&sort_by=popularity.desc"
    movie_api = MovieAPI(api_url_user_request)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)


def popular_movie_filter():
    """Filter popular movies."""
    print("Currently the most popular Movies are")
    popular_movie_url = f"/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    movie_api = MovieAPI(popular_movie_url)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)


def search_movie_filter():
    """This Function allows for users to Search for movies by the title"""
    while True:
        print("What Movie Would you like to view")
        movie_searched = input(":")
        search_movie_url = f"/3/search/movie?query={movie_searched}"
        movie_api = MovieAPI(search_movie_url)
        movie_data = movie_api.get_movie_info()
        if movie_data is not None:
            if len(movie_data.get('results', [])) > 0:
                print("Heres your Movies related to", movie_searched)
                movie_appending_and_printing_system(movie_data)
            else:
                print("That Movie does not exsist, please make sure you are choosing a real Movie")
        else:
            print("Failed to fetch movie data")


def menu():
    """Display the main menu for users with options so they can then choose a function to execute"""
    print("\nWhat action would you like to execute?")
    print("Type 1 if you would like to find a Movie")
    print("Type 2 to view your Favourites Watchlist")
    print("Type 3 if you would like to leave\n")
    user_choice = number_input_validation("Please Select an option", 1, 3)
    if user_choice == 1:
        movie_filter_selection()
    if user_choice == 2:
        getting_watchlist_to_object()
    if user_choice == 3:
        sys.exit()


def movie_filter_selection():
    """Display options for filtering movies such as by year, genre, popularity and even search by title"""
    print("\nHow would you like to filter to find a Movie?")
    print("Type 1 if you want to Filter by year")
    print("Type 2 Filter by Genre")
    print("Type 3 To get Popular Movies")
    print("Type 4 Search for a Movie\n")
    movie_filter_choice = number_input_validation("Please select an Option", 1, 4)
    if movie_filter_choice == 1:
        year_movie_filter()
    elif movie_filter_choice == 2:
        genre_movie_filter()
    elif movie_filter_choice == 3:
        popular_movie_filter()
    elif movie_filter_choice == 4:
        search_movie_filter()

#The Begining point of my Program where it prints our basic infomation and the brings the user to the Menu function
print("Welcome to Tom's Movie finder")
print("In this program you will be able filter through Movies find your favourites!")
print("At Any moment if you wish to return to the menu simply type 0")
print("Enjoy")
menu()