import requests
import sys
import config

class MovieAPI:
    def __init__(self, user_url_input):
        self.base_url = "https://api.themoviedb.org"
        self.user_url_input = user_url_input
        self.api_key = config.API_KEY

    def get_movie_info(self):
        endpoint = self.base_url + self.user_url_input + f"&api_key={self.api_key}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print("API call failed")
            return None

class UsersWatchlist:
    def __init__(self):
        self.watchlist_list = []

    def add_movies_to_watchlist(self, user_movie):
        self.watchlist_list.append(user_movie)

    def watchlist(self):
        length_of_watchlist = len(self.watchlist_list)
        if length_of_watchlist == 0:
            print("Currently there's no Movies in your Watchlist")
            menu()
        else:
            for watch in range(length_of_watchlist):
                print("Movie Number", watch + 1, self.watchlist_list[watch])
        menu_or_remove = string_input_validation("Please type Remove to remove items from your watchlist, if you do not want to do this please type Menu", "REMOVE", "MENU", "Please Choose a Valid Option which is Remove or Menu")
        if menu_or_remove == "MENU":
            print("Now returning to the Menu")
        elif menu_or_remove == "REMOVE":
            self.remove_movies_from_watchlist()

    def remove_movies_from_watchlist(self):
        remove_movie_number = number_input_validation("Looking at the Movie Number please enter the Movie Number of the Movie you would like to remove, type 0 if you would like to return to Menu", 0, len(self.watchlist_list))
        if remove_movie_number == 0:
            menu()
        else:
            del self.watchlist_list[remove_movie_number - 1]
        remove_something_else = string_input_validation("Please type Remove to remove more items from your watchlist, if you do not want to do this please type Menu", "YES", "NO", "Please Choose a Valid Option which is Yes or No")
        if remove_something_else == "YES":
            self.remove_movies_from_watchlist()
        elif remove_something_else == "NO":
            menu()

def number_input_validation(msg, minimum, maximum):
    print(msg)
    while True:
        try:
            user_response = int(input(":"))
            if minimum <= user_response <= maximum:
                return user_response
            else:
                print("That item is not in range")
        except ValueError:
            print("Invalid answer")

def string_input_validation(msg, option1, option2, invalid_select_option1_or_2):
    while True:
        try:
            users_choice = input(msg)
            users_choice = users_choice.upper()
            if users_choice == option1 or users_choice == option2:
                return users_choice
            else:
                print(invalid_select_option1_or_2)
        except Exception as e:
            print(e)

   

def movie_appending_and_printing_system(movie_data):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {"accept": "application/json", "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YmQ3YzJjNTg0ZmIwMzA2NWFmMjQ1YjY4NGQxNWFkMSIsInN1YiI6IjY2MDRkMGU3MTVkZWEwMDE4NTI3NmU0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URJ1s8L_2rhk4quhJbuXHzajszCJN58mpX1u1vvP8uU"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        genre_dict = response.json()
        genre_names = {genre['id']: genre['name'] for genre in genre_dict.get('genres', [])}
    else:
        print("Failed to fetch genre data.")
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
        the_movie_user_wants = number_input_validation("Looking at the ID numbers above, would you like to add a Movie to your watchlist? Type 0 to return to the menu: ", 0, len(movie_data['results']))
        if the_movie_user_wants == 0:
            menu()
        watchlist = UsersWatchlist()
        watchlist.add_movies_to_watchlist(movie_info_list[the_movie_user_wants - 1])
        menu()


def year_movie_filter():
    movie_year = number_input_validation("What years Movies do you want to filter through, I offer from 2000 - 2024", 2000, 2024)
    api_url_user_request = f"/3/discover/movie?primary_release_year={movie_year}"
    movie_api = MovieAPI(api_url_user_request)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)


def genre_movie_filter():
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
    movie_genre = number_input_validation("Please choose a response",1, 19)
    movie_genre = movie_genre - 1
    users_chosen_genre = genre_ids[movie_genre]
    api_url_user_request = f"/3/discover/movie?with_genres={users_chosen_genre}&sort_by=popularity.desc"
    movie_api = MovieAPI(api_url_user_request)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)

    

def popular_movie_filter():
    print("Currently the most popular Movies are")
    popular_movie_url = f"/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    movie_api = MovieAPI(popular_movie_url)
    movie_data = movie_api.get_movie_info()
    movie_appending_and_printing_system(movie_data)

def search_movie_filter():
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
    print("\nWhat action would you like to execute?")
    print("Type 1 if you would like to find a Movie")
    print("Type 2 to view your Favourites Watchlist")
    print("Type 3 if you would like to leave\n")
    user_choice = number_input_validation("Please Select an option", 1, 3)
    if user_choice == 1:
        movie_filter_selection()
    if user_choice == 2:
        watchlist_version = UsersWatchlist()
        watchlist_version.watchlist()  
    if user_choice == 3:
        sys.exit()

def movie_filter_selection():
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

print("Welcome to Tom's Movie finder")
print("In this program you will be able filter through Movies find your favourites!")
print("Enjoy")
menu()