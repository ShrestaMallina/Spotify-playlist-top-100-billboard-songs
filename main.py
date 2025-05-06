from pprint import pprint

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
ENDPOINT_PRIVATE_LIST = "https://api.spotify.com/v1/me"
CLIENT_ID = "3b03b78d398a4dbd98274a197f05e011"
CLIENT_SECRET = "48f24bc6f79c4ad0b5dda8e0dc5eee45"
SPOTIFY_USERNAME = "Shresta Mallina"

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
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
        redirect_uri="https://example.com/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USERNAME,
    )
)
user_id = sp.current_user()["id"]
#print(user_id)#314bmmtn72pgu535au2k7zm5dgje
song_uris =[]
for song in list_100:
    result = sp.search(q=f"track:{song} year:{"2017-05-06"}",type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        pprint(song_uris)


    except IndexError:
        pass
        #pprint(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"2017-05-06 Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)












