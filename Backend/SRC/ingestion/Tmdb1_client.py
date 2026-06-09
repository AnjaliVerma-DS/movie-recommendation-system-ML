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

        all_movie=[]
        for page in range(1,59):
            print(f"fetching page {page}")
            try:
                response = requests.get(
                    url=url,
                    params={
                         "api_key": self.api_key,
                         "page": page
                         }
                         )
                response.raise_for_status()
                response_data=response.json()
                
                all_movie.extend(response_data['results'])
        

            except Exception as e:
                print(" got exception while running init_client:", e)
                continue
            print("Total movies collected:", len(all_movie))
        return {"results": all_movie}


if __name__ == "__main__":

    client = TMDBClient(
        api_key=os.getenv("TMDB_API_KEY"),
        base_url=os.getenv("BASE_URL")
    )

    resp = client.init_client("discover/movie")

    print(resp)

    # save JSON 
    if resp:
        data_dir = Path("../../data")
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(data_dir / "tmdb_response.json", "w") as f:
         json.dump(resp, f, indent=4)
         print("JSON Path:", (data_dir / "tmdb_response.json").resolve())
         print("CSV Path:", (data_dir / "tmdb_response.csv").resolve())


    # CREATE DATAFRAME 
    if resp and "results" in resp:

        df = pd.DataFrame(resp["results"])

        print("\n DATAFRAME CREATED\n")
        print(df.head())
        print(df.info())
        print(df.describe())
        print(len(df))
               
        df.to_csv(data_dir / "tmdb_response.csv", index=False)

    else: 
        print(" DataFrame not created (API issue)")

