import requests, config, sys

class movieapi:
    def __init__(self,user_url_input):
        self.base_url = "http://www.omdbapi.com/?"
        self.user_url_input = user_url_input


    def get_movie_info(self):
            url = self.base_url + self.user_url_input
            url += f"?limit={200}"
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                return json_data
            else:
                print("API call failed.")
                return None


class Users_Watchlist:
    def __init__(self):
        self.watchlist_list = []
        
    
    def add_movies_to_watchlist(self, user_movie):
        self.watchlist_list.append(user_movie)

    
    def watchlist(self):
        length_of_watchlist = len(self.watchlist_list)
        if length_of_watchlist == 0:
            print("Currently theirs no Movies in your Watchlist")
            menu()
        else:
            for watch in length_of_watchlist:
                print("Movie Number",watch + 1 ,self.watchlist_list[watch])
        menu_or_remove = string_input_validation("Please type Remove to remove items from your watchlist, if you do not want to do this please type Menu","REMOVE","MENU","Please Choose a Valid Option which is Remove or Menu")
        if menu_or_remove == "MENU":
            print("Now returning to the Menu")
        elif menu_or_remove == "REMOVE":
            self.remove_movies_from_watchlist()


    def remove_movies_from_watchlist(self):
        remove_movie_number = number_input_validation("Looking at the Movie Number please the Movie Number of the Movie you would like to remove, type 0 if you would like to return to Menu", 0 , len(self.watchlist_list))
        if remove_movie_number == 0:
            menu()
        else:
            del self.watchlist_list[remove_movie_number - 1]
        remove_something_else = string_input_validation("Please type Remove to remove items from your watchlist, if you do not want to do this please type Menu","YES","NO","Please Choose a Valid Option which is Yes or No")
        if remove_something_else == "YES":
            self.remove_movies_from_watchlist
        elif remove_something_else == "NO":
            menu()


def number_input_validation(msg, minimum, maximum): 
    print(msg)
    while True:
        try:
            user_response = int(input(":"))
        except ValueError:
            print("Invalid answer")
            continue
        if user_response < minimum or user_response > maximum:
            print("That item is not in range")
            continue
        else:
            return user_response

def string_input_validation(msg, option1, option2, invalid_select_option1_or_2):
  while True:
    try:
      users_choice = input(msg)
      users_choice = users_choice.upper()
      if users_choice == option1:
        return users_choice
      if users_choice == option2:
        return users_choice
      else:
        print(invalid_select_option1_or_2)
    except:
      print(invalid_select_option1_or_2)

        
#def year_movie_filter():
#def genre_movie_filter():
#def rated_movie_filter():
#def search_movie_filter()

def menu():
    print("\nWhat action would you like to execute?")
    print("Type 1 if you would like to find a Movie")
    print("Type 2 to view your Favourtes Watchlist")
    print("Type 3 if you would like to leave\n")
    user_choice = number_input_validation("Please Select a option", 3, 1)
    if user_choice == 1:
        movie_filter_selection()
    if user_choice == 2:
        "function for user to view their favourites list which is the watchlist function in User_Watchlist object"
    if user_choice == 3:
        sys.exit
     

def movie_filter_selection():
    print("\nHow would you like to filter to find a Movie?")
    print("Type 1 if you want to Filter by year")
    print("Type 2 Filter by Genre")
    print("Type 3 Filter by Rated(e.g P.G 13)")
    print("Type 4 Search for a Movie\n")
    movie_filter_choice = number_input_validation("Please select a Option", 1 , 4)
    if movie_filter_choice == 1:
        year_movie_filter()
    elif movie_filter_choice == 2:
        genre_movie_filter()
    elif movie_filter_choice == 3:
        rated_movie_filter()
    elif movie_filter_choice == 4:
        search_movie_filter()




print("Welcome to Tom's Movie finder")
print("In this program you will be able filter through Movies find your favourites!")
print("Enjoy")
menu()