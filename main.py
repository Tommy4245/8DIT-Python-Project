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
                print(self.watchlist_list[watch])




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
        
        

def menu():
    print("What action would you like to execute?")
    print("Type 1 if you would like to find a Movie")
    print("Type 3 to view your Favourtes Watchlist")
    print("Type 2 if you would like to leave")
    user_choice = number_input_validation("Please Select a option", 3, 1)
    if user_choice == 1:
        "filter function with the next menu"
    if user_choice == 2:
        "function for user to view their favourites list"
    if user_choice == 3:
        sys.exit
     

def movie_filter_selection():
    print("How would you like to filter to find a Movie?")
    print("Type 1 if you want to Filter by year")

    print("Type 2 Filter by Genre")

    print("Type 3 Filter by Rated(e.g P.G 13)")

    print("Type 4 Search for a Movie")


print("Welcome to Tom's Movie finder")
print("In this program you will be able filter through Movies find your favourites!")
print("Enjoy")
print("")
menu()