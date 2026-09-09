import pandas as pd
import requests

# Tworzenie DataFrame z listą wykonawców
data = {'Artist': ['Red Hot Chilli Peppers','Bedoes','Metallica','Gojira','Gorillaz','Linkin Park','AC/DC','Michael Jackson']}
df = pd.DataFrame(data)
df = pd.read_csv(r"D:\Users\User\Desktop\Studia\MGR\SEM 2\MEIAD\Spotify_Youtube.csv")
# Funkcja do pobierania gatunku muzycznego z Last.fm
artist = pd.DataFrame(df['Artist'][0:100])
print(artist)
def get_music_genre(artist):
    api_key = 'a35185554dcf6d7b7a76c514ba345975'  # Zarejestruj się na stronie Last.fm, aby uzyskać klucz API
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'artist.getinfo',
        'artist': artist, #pd.DataFrame(df['Artist'].unique()),
        'api_key': api_key,
        'format': 'json'
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if 'error' in data:
        return 'Błąd'
    elif 'artist' in data and 'tags' in data['artist'] and 'tag' in data['artist']['tags']:
        tags = data['artist']['tags']['tag']
        if tags:
            return tags[0]['name']  # Zwróć pierwszy gatunek
        else:
            return 'Brak informacji'
    else:
        return 'Brak informacji'

# Dodanie nowej kolumny z gatunkiem do DataFrame
artist['Genre'] = artist['Artist'].apply(get_music_genre)

# Wyświetlenie DataFrame z gatunkami
print(artist)
