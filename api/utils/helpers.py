import requests

class Song:
    def __init__(self, data: dict):
        """init for Song class

        Args:
            data (dict): dictionary of song info. Formatted according to Spotify's web API for tracks
        """
        self.artist_name = data["artists"][0]["name"]
        self.artist_id = data["artists"][0]["id"]
        self.name = data["name"]
        self.id = data["id"]

    def json(self):
        """returns dict of object data in json format
        """

        return {
            "artist_name": self.artist_name,
            "artist_id": self.artist_id,
            "name": self.name,
            "id": self.id
        }


def get_user_playlists(token: str):
    """[summary]

    Args:
        token ([type]): [description]

    Returns:
        [type]: [description]
    """

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)

    if not response:
        return Response(data="Could not get playlists", status=502)

    information = response.json()

    playlists = []

    for playlist in information["items"]:
        id = playlist["id"]
        name = playlist["name"]

        song_response = requests.get(f"https://api.spotify.com/v1/playlists/{id}/tracks?market=US", headers=headers)

        if not song_response:
            return Response(data="Could not get song response", status=502)

        song_info = song_response.json()

        songs = []
        for item in song_info["items"]:
            song = Song(item["track"])
            songs.append(song.json())

        playlists.append({
            name: songs
        })
    
    return playlists