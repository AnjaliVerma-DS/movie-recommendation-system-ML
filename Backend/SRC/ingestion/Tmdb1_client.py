import os
import dotenv
import requests
import json
from pathlib import Path
import pandas as pd

dotenv.load_dotenv()


class TMDBClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def init_client(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(
                url=url,
                params={
                    "api_key": self.api_key,
                    "page": 1
                }
            )

            response.raise_for_status()
            response_data=response.json()

            return  response_data
        

        except Exception as e:
            print(" got exception while running init_client:", e)

if __name__ == "__main__":

    client = TMDBClient(
        api_key=os.getenv("TMDB_API_KEY"),
        base_url=os.getenv("BASE_URL")
    )

    resp = client.init_client("discover/movie")

    print(resp)

    # save JSON 
    if resp:
        with open("tmdb_response.json", "w") as f:
            json.dump(resp, f, indent=4)

    # CREATE DATAFRAME 
    if resp and "results" in resp:

        df = pd.DataFrame(resp["results"])

        print("\n DATAFRAME CREATED\n")
        print(df.head())

        df.to_csv("tmdb_response.csv", index=False)

    else:
        print(" DataFrame not created (API issue)")