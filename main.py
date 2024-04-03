import requests #Imports the requests package, this allows me to make my API calls
import os  #Imports os so I am to close the program if a user does not meet the requirments for it to run
import config #This is imported from another local file and contains my API Key

try: #This script just checks to see if a user has the write software on there computer to see if they can run it
    import requests
except ImportError:
    print("Please install the requests package by running")
    print("pip install requests")
    print("This program can not run without the requests package")
    print("Exiting...")
    os._exit(1)

watchlist_to_make_instances = [] #Stores all the users infomation about the movies they have in there watchlist

class MovieAPI:
    """Class to interact with the Movie Database API being TMDb"""
    """The Goal for this Class is to retreive data from my TMDb API"""
    """The Data then is going to get returned to other functions in the Code so the User can decide what Movies they like"""

    def __init__(self, user_url_input):
        """Initialize MovieAPI object by useing __init__ with base URL and API key from config.py"""
        self.base_url = "https://api.themoviedb.org" #This is the TMDb base URL
        self.user_url_input = user_url_input  #This instance is a URL that is made by one of the filter functions to become the endpoint
        self.api_key = config.API_KEY #This key is my API Key and is essential to have when useing TMDb, because of this it's private to me so its saved in a different Python program as its private infomation, for any user wanting to use my code you will need to generate your own key

    def get_movie_info(self):
        """This Function makes a endpoint and then Fetches key infomation from the TMDb API"""
        endpoint = self.base_url + self.user_url_input + f"&api_key={self.api_key}" #This is my endpoint which is my URL in my API that my requests function is going to call
        try:
            response = requests.get(endpoint) #This is the call for the data from my API
        except:
            print("API call failed, Please check your internet is working and you have disabled any website blockers") #This is here incase the API call fails due to potentially internet issues ect, this catches the code before the program crashes
            os._exit(1)
        if response.status_code == 200: #If the status code is 200 we know the API call was sucsessful which then allows us to return the data requested to where it was called
            json_data = response.json()
            return json_data
        else: 
            print("API call failed") #This just some extra robustness incase somehow invalid infomation escapes the first input validation, this explicitly check if the code is 200 and if it isn't the code indicates that something went wrong
            os._exit


class UsersWatchlist:
    """Class which allows the user to manage and modify movies in there watchlist"""
    
    def __init__(self):
        """Initalizes the Object by useing __init__ and makeing a empty list for the users watchlist"""
        self.watchlist_list = [] #This is a list which contains all the instances of Movies in the users Watchlist

    def add_movies_to_watchlist(self, movie_title, movie_rating, movie_genre, movie_overview):
        """Makes all the instances of data the User needs for the Watchlist then appends it to the empty list"""
        self.watchlist_list.append([movie_title, movie_rating, movie_genre, movie_overview]) #Appends all the users Movie info into the watchlist list

    def watchlist(self):
        """This Function displays the Users Watchlist by printing out the self.watchlist_list, it also allows for the user to modify the list"""
        length_of_watchlist = len(self.watchlist_list)
        if length_of_watchlist == 0: #Checks to see if the user actually has anything in there watchlist and if they don't the function shall not proceed 
            print("Currently there are no movies in your watchlist")
            print("Returning to Menu")
            menu()
        else:
            for watch, movie_info in enumerate(self.watchlist_list): #Identifys how many items are in the watchlist list and then prints them out formatted
                print("\nID Number:", watch + 1)
                print("Title:", movie_info[0])
                print("Rating:", movie_info[1])
                print("Genre:", movie_info[2])
                print("Overview:", movie_info[3])
        menu_or_remove = string_input_validation("Please type Remove to remove items from your watchlist, if you do not want to do this please type Menu to return to the menu", "REMOVE", "MENU", "Please Choose a Valid Option which is Remove or Menu") #checks to see if the user would like to remove infomation from there watchlist or return to the menu
        if menu_or_remove == "MENU":
            print("Now returning to the Menu")
            menu()
        elif menu_or_remove == "REMOVE":
            self.remove_movies_from_watchlist() #Brings the User to remove items from watchlist function

    def remove_movies_from_watchlist(self):
        """Allows for the user to remove items from there watchlist"""
        remove_movie_number = number_input_validation("Looking at the Movie ID Number please enter the Movie ID Number of the Movie you would like to remove", 1, len(self.watchlist_list)) #Gets the user to select what movie they would like to remove from their watchlist
        del watchlist_to_make_instances[remove_movie_number - 1]
        print("Your New Watchlist is")
        getting_watchlist_to_object() #Runs the watchlist function again and updates the instances so we get a new list of Movies currently in the Users watchlist and then repeats the process of asking if the user would like to remove anything from there cart 
        
        '''remove_something_else = string_input_validation("Would you like to Remove anything else, please type 'yes' or 'no'", "YES", "NO", "Please Choose a Valid Option which is Yes or No") #Asks the user if they would like to remove more movies from the watchlist or not 
        if remove_something_else == "YES":
            getting_watchlist_to_object()
            self.remove_movies_from_watchlist()
        elif remove_something_else == "NO":
            print("Returning to menu")
            menu()'''

def number_input_validation(msg, minimum, maximum):
    """Validate int values that the user has selected and has boundarys to validate the user response is in range, also allows the user to return to the menu at any time if they type 0
    msg (str): The message that prompts the User at the start
    minimum (int): The Minmum Value a User can input
    maximum (int): The Maximum Value a User can input
    """
    print(msg)
    while True:
        try:
            user_response = int(input(":")) #Gets the users response
            if user_response == 0: #If the awnser is 0 returns to Menu, follows the convention of my code for if a user types 0 at anypoint they will return to the menu
                menu()
            elif minimum <= user_response <= maximum: #Checks that the item is in range 
                return user_response
            else:
                print("That item is not in range")
        except ValueError:
            print("Invalid answer")

def string_input_validation(msg, option1, option2, invalid_select_option1_or_2):
    """Validate string input againts options by haveing 2 valid awnsers, also allows the user to return to the menu at any time if they type 0
    msg (str): The message prompt for the user.
    option1 (str): The first valid answer option.
    option2 (str): The second valid answer option.
    invalid_select_option1_or_2 (str): The message to display when the user selects an invalid option.
    """
    print(msg)
    while True:
        try:
            users_choice = input(":")
            if users_choice == "0":
                menu()
            users_choice = users_choice.upper() #Formats so all the results have the same case to avoid confusion and errors makeing my program Robust
            if users_choice == option1 or users_choice == option2: #Checks to see if the User has inputed a Valid choice
                return users_choice
            else:
                print(invalid_select_option1_or_2)
        except:
            print(invalid_select_option1_or_2)

def getting_watchlist_to_object():
    """Convert watchlist data into UsersWatchlist object by useing the external list watchlist_to_make_instances"""
    watchlist_version = UsersWatchlist() #Creates the New instance for my object for this Watchlist
    for watch in range(len(watchlist_to_make_instances)): #Finds out how many iterations of data is going to be sent to the Watchlist object then loops through them
        title = watchlist_to_make_instances[watch][0]
        rating = watchlist_to_make_instances[watch][1]
        genre = watchlist_to_make_instances[watch][2]
        overview = watchlist_to_make_instances[watch][3]
        watchlist_version.add_movies_to_watchlist(title, rating, genre, overview) #sends my data to my object makeing a new instance
    watchlist_version.watchlist() #Displays my watchlist by going to the function


def movie_appending_and_printing_system(movie_data):
    """Append movie data to the watchlist_to_make_instances external list and prints data from the API so a User can decide what movies they want to add to there watchlist"""
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {"accept": "application/json", "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0YmQ3YzJjNTg0ZmIwMzA2NWFmMjQ1YjY4NGQxNWFkMSIsInN1YiI6IjY2MDRkMGU3MTVkZWEwMDE4NTI3NmU0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URJ1s8L_2rhk4quhJbuXHzajszCJN58mpX1u1vvP8uU"}
    try:
        response = requests.get(url, headers=headers) #Gets the genres dictionary from the TMDb API
    except:
        print("API call failed, Please check your internet is working and you have disabled any website blockers") #This is here incase the API call fails due to potentially internet issues ect, this catches the code before the program crashes
        os._exit(1)
    if response.status_code == 200: #Checks that it went sucsessfully 
        genre_dict = response.json() 
        genre_names = {genre['id']: genre['name'] for genre in genre_dict.get('genres', [])} #Makes the Dictionary translatible for me so I can find genres in aquantince to their Key
    else:
        print("Failed to fetch genre data, API Call Failed") #Backup just incase something doesn't get picked up in my first input validation
        menu()           
    if movie_data: #Easy way to make sure that there is data from the API 
        movie_info_list = [] #Creates a list that will contain all the movies sent from the API
        for id_number, movie in enumerate(movie_data['results']): #creates a for i in range loop so all the data from the API can be printed out formatted and also appended to the list
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
        the_movie_user_wants = number_input_validation("Looking at the ID numbers above, would you like to add a Movie to your watchlist? Rember to type 0 if you would not like to so you can return to the menu", 1, len(movie_data['results'])) #Gets the User to add any movies they would like in their watchlist
        watchlist_to_make_instances.append(movie_info_list[the_movie_user_wants - 1]) #Appends the Movie that the user wants to the external list being watchlist_to_make_instances
        menu()


def year_movie_filter():
    """Filters Movies by there release Year, I have given the user the option to select Movies from 2000 - 2024"""
    movie_year = number_input_validation("What years Movies do you want to filter through, I offer from 2000 - 2024", 2000, 2024) #Gets the user to select a Movie between the desired range of 2000 - 2024
    api_url_user_request = f"/3/discover/movie?primary_release_year={movie_year}" #makes the second half of the endpoint URL
    movie_api = MovieAPI(api_url_user_request) #makes instance
    movie_data = movie_api.get_movie_info() #requests the data from the API
    movie_appending_and_printing_system(movie_data) #Brings us to the printing system where a user can see all there movies and select ones they would like to add to there watchlist


def genre_movie_filter():
    """Filters Movies by Genre"""
    genre_ids = [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37] #This is a list that allows that allows me to link the users response to the dictionary key in TMDb for genres 
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
    movie_genre = movie_genre - 1 #figures out the index number in the list above and therefore assoicates the correct genre with its key
    users_chosen_genre = genre_ids[movie_genre] #Gets the genre key
    api_url_user_request = f"/3/discover/movie?with_genres={users_chosen_genre}&sort_by=popularity.desc" #makes the second half of the endpoint/url
    movie_api = MovieAPI(api_url_user_request) #makes instance
    movie_data = movie_api.get_movie_info() #requests the data from the API
    movie_appending_and_printing_system(movie_data) #Brings us to the printing system where a user can see all there movies and select ones they would like to add to there watchlist

def popular_movie_filter():
    """Filter popular movies."""
    print("Currently the most popular Movies are")
    popular_movie_url = f"/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc" #the second half of the url/endpoint for popular movies
    movie_api = MovieAPI(popular_movie_url) #makes instance
    movie_data = movie_api.get_movie_info() #requests the data from the API
    movie_appending_and_printing_system(movie_data) #Brings us to the printing system where a user can see all there movies and select ones they would like to add to there watchlist

def search_movie_filter():
    """This Function allows for users to Search for movies by the title"""
    while True:
        print("What Movie Would you like to view") 
        movie_searched = input(":") #gets the user to input a movie that they would like to view
        search_movie_url = f"/3/search/movie?query={movie_searched}" #makes the second half of the endpoint/url
        movie_api = MovieAPI(search_movie_url) #makes instance
        movie_data = movie_api.get_movie_info() #requests the data from the API
        if movie_data is not None: #checks to see if there where any results with the search that was made
            if len(movie_data.get('results', [])) > 0: #checks to see if any infomation was in the movie_data varible that was sourced from the API
                print("Heres your Movies related to", movie_searched)
                movie_appending_and_printing_system(movie_data) #Brings us to the printing system where a user can see all there movies and select ones they would like to add to there watchlist
            else:
                print("That Movie does not exsist, please make sure you are choosing a real Movie and also check your spelling") #If there was no movie that even related to the input from the user the user will be prompt here and then asked to choose a movie that exsits


def menu():
    """Display the main menu for users with options so they can then choose a function to execute"""
    print("\nWhat action would you like to execute?")
    print("Type 1 if you would like to find a Movie")
    print("Type 2 to view your Favourites Watchlist")
    print("Type 3 if you would like to leave\n")
    user_choice = number_input_validation("Please Select an option", 1, 3) #Gets the users option for what they would currently like to do in the program
    if user_choice == 1:
        movie_filter_selection()
    if user_choice == 2:
        getting_watchlist_to_object()
    if user_choice == 3:
        os._exit(1)


def movie_filter_selection():
    """Display options for filtering movies such as by year, genre, popularity and even search by title"""
    print("\nHow would you like to filter to find a Movie?")
    print("Type 1 if you want to Filter by year")
    print("Type 2 Filter by Genre")
    print("Type 3 To get Popular Movies")
    print("Type 4 Search for a Movie\n")
    movie_filter_choice = number_input_validation("Please select an Option", 1, 4) #Gets the users option for what they want to filter by for movies in the program
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