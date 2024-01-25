import requests
import pandas as pd
import time
from decouple import config
import ast

config_path = ".env"
api_key = config("API_KEY", default = "")

def get_puuids():

    # Replace 'YOUR_API_KEY' with the API key you obtained from the Riot Developer Portal


    # Construct the API request URL for summoner information
    url = f'https://na1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT&api_key={api_key}'
    
    # Make the API request
    response = requests.get(url)
    puuid = []
    # Check if the request was successful (status code 200)

    if response.status_code == 200:
        # Parse the JSON response
        summoner_name = [summoner["summonerName"] for summoner in response.json()["entries"]]
        ine = 0
        for name in summoner_name:
            puuid_url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}'
            puuid_response = requests.get(puuid_url)
            if puuid_response.status_code == 200:
                puuid.append(puuid_response.json()["puuid"])
                with open("puuid.txt", "a") as file:
                    file.write(f"{puuid_response.json()['puuid']}\n")
                time.sleep(1)
                ine += 1
            else:
                print(f'Error getting puuid: {name}')
                
    else:
        print(f"Error: {response.status_code}")

def get_matches():
    with open("puuid.txt", "r") as file:
        match_ids = set([])
        lst = file.readlines()
        ads =0 
        for ids in lst:
            ids = ids.strip()
            match_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{ids}/ids?start=0&count=20&api_key={api_key}"
            match_response = requests.get(match_url)
            if match_response.status_code == 200:
                for match_id in match_response.json():
                    match_ids.add(match_id)
                time.sleep(1)
            else:
                print(f'Error getting matches for {ids}: {match_response.status_code}')

        with open("match_ids.txt", "a") as file:
            for match_id in match_ids:
                file.write(f"{match_id}\n") 


def to_csv():

    with open("match_ids.txt", "r") as file:
        match_ids = [line.strip() for line in file]

        # Make API requests and save data to CSV
        all_data = []
        index = 0 
        for match_id in match_ids:
            url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"
            response = requests.get(url)
            time.sleep(1)
            if response.status_code == 200:
                match_data = response.json()

                all_data.append(pd.json_normalize(match_data))
            else:
                print(f"Error for match_id {match_id}: {response.status_code}")
        

        combined_data = pd.concat(all_data, ignore_index=True)

        # Save combined data to a single CSV file
        combined_data.to_csv("combined_data.csv", index=False)



def get_augment():
    url = 'https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/tft-augments.json'
    response = requests.get(url)

    print(response.json())



def main():

    get_augment()
    '''
    df = pd.read_csv("combined_data.csv")
    df['info.participants'] = df['info.participants'].apply(ast.literal_eval)
    first_row = df['info.participants'].iloc[0]

    print(first_row[0])
    '''

main()


    




        