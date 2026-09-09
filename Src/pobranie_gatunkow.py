import pandas as pd
import requests

# Tworzenie DataFrame z listą wykonawców
data = {'Artist': ['Red Hot Chilli Peppers','Bedoes','Metallica','Gojira','Gorillaz','Linkin Park','AC/DC','Michael Jackson']}
df = pd.DataFrame(data)
df = pd.read_csv(r"D:\Users\User\Desktop\Studia\MGR\SEM 2\MEIAD\Spotify_Youtube.csv")
do_wywalenia = [df.columns[0],'Uri','Url_spotify','Url_youtube','Title','Channel','Comments','Description','Licensed', 'official_video']
# df = df.drop[0]
df = df.drop(do_wywalenia,axis=1)
print(df.info())
print(df.isnull().sum())
# Funkcja do pobierania gatunku muzycznego z Last.fm
# artist = pd.DataFrame(df['Artist'][0:100])
# print(artist)

import musicbrainzngs

def get_music_genres_from_musicbrainz(artist_name):
    musicbrainzngs.set_useragent("MyMusicApp", "1.0", "example@email.com")
    print("wejszlem")
    requests.adapters.DEFAULT_RETRIES = 5  # Liczba ponownych prób
    requests.adapters.DEFAULT_TIMEOUT = 30
    print(artist_name)
    try:
        artist_info = musicbrainzngs.search_artists(artist=artist_name)
        if 'artist-list' in artist_info and len(artist_info['artist-list']) > 0:
            artist_id = artist_info['artist-list'][0]['id']
            artist_data = musicbrainzngs.get_artist_by_id(artist_id, includes=['tags'])
            
            if 'tag-list' in artist_data and len(artist_data['tag-list']) > 0:
                genres = [tag['name'] for tag in artist_data['tag-list']]
                return genres
            else:
                return ["Brak dostępnych gatunków"]
        else:
            return ["Nie znaleziono artysty"]
    except musicbrainzngs.ResponseError:
        return ["Błąd API MusicBrainz"]

# # Przykład użycia
# artist_name = "The Beatles"
# genres = get_music_genres_from_musicbrainz(artist_name)
# print(f"Gatunki muzyczne dla {artist_name}: {', '.join(genres)}")

def get_music_genres_for_artists(artist_names, timeout_seconds=10):
    musicbrainzngs.set_useragent("MyMusicApp", "1.0", "example@email.com")
    print("wszlem")
    # Dostosuj czas oczekiwania dla zapytań HTTP w module requests
    requests.adapters.DEFAULT_RETRIES = 10  # Liczba ponownych prób
    requests.adapters.DEFAULT_TIMEOUT = timeout_seconds  # Maksymalny czas oczekiwania w sekundach
    
    try:
        # Przygotuj listę nazw artystów
        artist_list = [{'name': artist_name} for artist_name in artist_names]

        # Wykonaj zapytanie do API MusicBrainz z listą artystów
        artist_info = musicbrainzngs.search_artists(artist=artist_list)
        
        # Przetwarzanie odpowiedzi i uzyskiwanie gatunków muzycznych
        genres = []
        for result in artist_info['artist-list']:
            if 'tag-list' in result:
                artist_genres = [tag['name'] for tag in result['tag-list']]
                genres.append(artist_genres)
            else:
                genres.append(["Brak dostępnych gatunków"])

        return genres
    except musicbrainzngs.ResponseError:
        return ["Błąd API MusicBrainz"]

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_with_retry(url, max_retries, timeout, params = None):
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url, params= params, timeout= timeout)
    return response

def get_music_genre(artist):
    api_key = 'a35185554dcf6d7b7a76c514ba345975' 
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'artist.getinfo',
        'artist': artist, #pd.DataFrame(df['Artist'].unique()),
        'api_key': api_key,
        'format': 'json'
    }
    
    response = get_with_retry(base_url, params=params, timeout=600, max_retries= 5)
    data = response.json()
    print(artist)
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


def get_music_genres_for_artists_LFM(artist_names):
    api_key = 'a35185554dcf6d7b7a76c514ba345975'
    endpoint = 'http://ws.audioscrobbler.com/2.0/'

    # Przygotuj listę nazw artystów
    artist_names_str = ','.join(artist_names)

    # Parametry zapytania
    params = {
        'method': 'artist.gettoptags',
        'artist': artist_names_str,
        'api_key': api_key,
        'format': 'json'
    }

    try:
        # Wykonaj zapytanie do API Last.fm
        response = requests.get(endpoint, params=params, timeout= 60)
        data = response.json()

        # Przetwarzanie odpowiedzi i uzyskiwanie gatunków muzycznych
        genres = []
        for artist_name in artist_names:
            if artist_name in data.get('toptags'):
                artist_tags = data['toptags'][artist_name]['tag']
                artist_genres = [tag['name'] for tag in artist_tags]
                genres.append(artist_genres)
            else:
                genres.append(["Brak dostępnych gatunków"])

        return genres
    except requests.exceptions.RequestException:
        return ["Błąd API Last.fm"]

import pickle


unique = df['Artist'].unique()

unique = pd.DataFrame({"Artist":unique})

unique["Genre"]= None
unique["Genre"] = unique["Artist"].apply(get_music_genre)

with open("art_gat.pkl",'wb') as plik:
    pickle.dump(unique,plik)

df = df.merge(unique, on='Artist', how='left')

with open("art_gat.pkl", 'rb') as plik:
    wczytany_df = pickle.load(plik)

# Teraz masz wczytany DataFrame w zmiennej wczytany_df
print(wczytany_df)


# df['Genre'] = None
# print("TU")
# df.loc[0:50, 'Genre'] =get_music_genre( df['Artist'][0:50])
# print("raz")
# df.loc[51:100, 'Genre'] =get_music_genre( df['Artist'][51:100])
# print("dwa")
# i = 101

# batch = 50
# for i  in range(0,1000,batch):
#     print(i," : ", i+batch)
#     df.loc[i:i+batch, 'Genre'] =df['Artist'][i:i+batch].apply(get_music_genre) #df['Artist'][i:i+batch]))
#     df.to_csv("muzyczka_z_gatunkami.csv",index=False)

# df['Genre'][1] = df['Artist'][1].apply(get_music_genre)
# df['Genre'] = None
# df.loc[0:40, 'Genre'] = get_music_genres_for_artists(df['Artist'][0:40],timeout_seconds=60)
# artists = ["Bedoes", "Red Hot Chilli Peppers", "Gorillaz"]
# lista_gatunkow = get_music_genres_for_artists_LFM(artist_names=artists)
# print(lista_gatunkow)
# Wyświetlenie DataFrame z gatunkami
print(df[['Artist','Genre']])
print(df.info())

df.to_csv("muzyczka_z_gatunkami.csv",index=False)
