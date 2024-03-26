import requests, config

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
