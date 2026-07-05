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
    
    def get_movie_details(self, movie_id: int):
        
        url = f"{self.base_url}/movie/{movie_id}"

        response = requests.get(
            url=url,
            params={
                "api_key": self.api_key
            }
        )

        response.raise_for_status()

        return response.json()
    
    def get_movie_credits(self, movie_id: int):
        
        url = f"{self.base_url}/movie/{movie_id}/credits"


        response = requests.get(
            url=url,
            params={
                "api_key": self.api_key
            }
        )
        
        response.raise_for_status()

        return response.json()
    
    def get_movie_keywords(self, movie_id: int):
        
        url = f"{self.base_url}/movie/{movie_id}/keywords"


        response = requests.get(
            url=url,
            params={
                "api_key": self.api_key
            }
        )
        
        response.raise_for_status()

        return response.json()


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

        rows = []

        for movie_id in df["id"][:10]:

            print(f"Processing: {movie_id}")

            details = client.get_movie_details(movie_id)
            credits = client.get_movie_credits(movie_id)
            keywords = client.get_movie_keywords(movie_id)

            genres = " ".join([g.get("name") for g in details.get("genres", [])])

            cast = " ".join([c.get("name") for c in credits.get("cast", [])])

            director = ""
            for c in credits.get("crew", []):
                if c.get("job") == "Director":
                    director = c.get("name")
                    break

            kw = " ".join([k.get("name") for k in keywords.get("keywords", [])])

            rows.append({
                "id": movie_id,
                "genres": genres,
                "cast": cast,
                "director": director,
                "keywords": kw
                })
            
            
            new_df = pd.DataFrame(rows)

            final_df = df.merge(new_df, on="id", how="left")


            print(final_df.head())
            print(final_df.info())
            print(final_df.columns)
               
            final_df.to_csv(data_dir /"tmdb_response.csv", index=False)
            final_df.to_json(data_dir /"tmdb_response.json", orient="records", indent=4)

    else: 
        print(" DataFrame not created (API issue)") 
