import pandas as pd
import requests
import base64
from tqdm import tqdm

# Replace these with your actual credentials
CLIENT_ID = 'c8e84b790b33494d9297f194b890a875'
CLIENT_SECRET = 'b8740812b4054acd800021dd23051ead'

def get_access_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json()["access_token"]

def get_album_cover_url(track_name, artist_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    query = f"track:{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1"
    response = requests.get(url, headers=headers)
    results = response.json().get("tracks", {}).get("items", [])
    if results:
        return results[0]["album"]["images"][0]["url"]
    return None

# Load your CSV (adjust encoding if needed)
df = pd.read_csv("spotify-2023.csv", encoding="ISO-8859-1")

token = get_access_token(CLIENT_ID, CLIENT_SECRET)
cover_urls = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    track = row["track_name"]
    artist = row["artist(s)_name"].split(",")[0]
    url = get_album_cover_url(track, artist, token)
    cover_urls.append(url)

df["album_cover_url"] = cover_urls
df.to_csv("spotify_with_album_covers.csv", index=False, encoding="utf-8")
print("✅ Done! File saved as: spotify_with_album_covers.csv")
