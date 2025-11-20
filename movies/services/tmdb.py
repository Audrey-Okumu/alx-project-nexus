import requests   # send HTTP requests to external APIs.
from django.conf import settings  # Imports my settings to import the TMDb Api key


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):   #runs when the class is created
        self.api_key = settings.TMDB_API_KEY
        self.session = requests.Session() # Creates a session for requests

    def _get(self, endpoint, params=None):
        """
        Internal GET request handler.
        Handles errors & adds API key automatically.
        """
        if params is None:
            params = {}

        params['api_key'] = self.api_key

        url = f"{self.BASE_URL}{endpoint}"
        
        print(f" Making request to {url}")  # Debug log
        print(f"  API Key exists: {bool(self.api_key)}")  # Debug log

        try:
            response = self.session.get(url, params=params, timeout=30)
            print(f"Response status: {response.status_code}")  # Debug log

            if response.status_code != 200:
                error_data = response.json()
                print(f" Error response: {error_data}")  # Debug log
                raise Exception(f"TMDB API Error {response.status_code}: {error_data}")

            data = response.json()
            print(f" Success! Got {len(data.get('results', []))} results")  # Debug log
            return data
            
        except requests.exceptions.RequestException as e:
            print(f" Request failed: {str(e)}")  # Debug log
            raise Exception(f"TMDB API Request failed: {str(e)}")

    # ===============================
    #           PUBLIC METHODS
    # ===============================

    def get_trending_movies(self):
        return self._get("/trending/movie/week")

    def get_movie_details(self, movie_id):
        return self._get(f"/movie/{movie_id}")

    def get_recommended(self, movie_id):
        return self._get(f"/movie/{movie_id}/recommendations")

    def search_movies(self, query: str):
        return self._get("/search/movie", params={"query": query})
