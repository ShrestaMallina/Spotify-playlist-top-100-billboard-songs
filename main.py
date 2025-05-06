from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
ENDPOINT_PRIVATE_LIST = "your spotify playlist api endpoint"
CLIENT_ID = "spotify client id"
CLIENT_SECRET = "spotify cilent sceret token"
SPOTIFY_USERNAME = "your spotify username"

header = {"your HTTP Header"}
#time_travel =input("which year would like to time travel? Type in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/2017-05-06/",headers=header)
billB_webpage = response.text

soup = BeautifulSoup(billB_webpage,"html.parser")
songs_list = soup.find_all(name="h3", id="title-of-a-story",class_="a-no-trucate")
list_100 = [song_name.getText().strip() for song_name in songs_list[:100]]
#print(list_100)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="your redirect uri in spotify",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USERNAME,
    )
)
user_id = sp.current_user()["id"]

song_uris =[]
for song in list_100:
    result = sp.search(q=f"track:{song} year:{"2017-05-06"}",type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        #pprint(song_uris)


    except IndexError:
        pass
        pprint(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"2017-05-06 Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)












