import requests
import pandas
import base64
from datetime import date,datetime,timedelta
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json
import configs
from SpotifyAPI import SpotifyAPI

#Connect to MySQL DB

connection = mysql.connector.connect(host = "mysql_db", database = "jason", user = "user", password = "password")

client_id = configs.client_id
client_secret = configs.client_secret
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())  #To change this string to base64 encoded string

# do a lookup for a token, this token is for future requests
token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = { 
        "grant_type" : "client_credentials"
}
token_headers = {
        "Authorization" : f"Basic {client_creds_b64.decode()}"
}


#Call object and perform authorization
spotify = SpotifyAPI(client_id, client_secret)

spotify.perform_auth()
print(spotify.perform_auth())
access_token = spotify.access_token

#Use Access Token to access Spotify API
header = {
    "Authorization" : f"Bearer {access_token}"
}

endpoint = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"
r = requests.get(endpoint, headers = header)
print(r.status_code)


data = r.json()
playlist_json = data['tracks']
playlist_data = []

for i in range(playlist_json['total']):
    
    artist_name = ''
    for j in range(len(playlist_json['items'][i]['track']['artists'])):
        artist_name = artist_name + ',' + data['tracks']['items'][i]['track']['artists'][j]['name']
    
    track_tuple = (artist_name[1:],
                   playlist_json['items'][i]['track']['id'],
                   playlist_json['items'][i]['track']['name'],
                   playlist_json['items'][i]['track']['duration_ms'],
                   playlist_json['items'][i]['track']['explicit'],
                   playlist_json['items'][i]['track']['popularity'],
                   i + 1,
                   playlist_json['items'][i]['track']['album']['id'],
                   playlist_json['items'][i]['track']['album']['name'],
                   playlist_json['items'][i]['track']['album']['album_type'],
                   playlist_json['items'][i]['track']['album']['release_date'],
                   datetime.today().strftime('%Y-%m-%d')
                    )
    
    playlist_data.append(track_tuple)

#Insert data into MySQL 
insert_query = """INSERT INTO spotify_daily_top_50_global (artist_name, track_id, track_name, duration_ms, explicit, popularity, daily_rank, album_id, album_name, album_type, release_date, dt)    
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
insert_data = playlist_data

try: 
    cursor = connection.cursor()
    cursor.executemany(insert_query,insert_data)
    connection.commit()
    print(cursor.rowcount,"Record inserted successfully into spotify_daily_top_50_global table")
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

