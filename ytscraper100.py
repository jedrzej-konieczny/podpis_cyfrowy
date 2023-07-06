import random
import time
import math
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

def pobierz_dlugosci_komentarzy(api_key, video_ids, max_comments_per_video):
    youtube = build('youtube', 'v3', developerKey=api_key)

    wszystkie_dlugosci_komentarzy = []

    for video_id in video_ids:
        # Pobierz pierwsze 100 komentarzy
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        while 'items' in response and len(wszystkie_dlugosci_komentarzy)<max_comments_per_video:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment_length = len(comment)
                wszystkie_dlugosci_komentarzy.append(comment_length)

            if 'nextPageToken' in response:
                # Jeżeli istnieje kolejna strona komentarzy, pobierz ją
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
            else:
                # Jeżeli nie ma kolejnej strony, zakończ pętlę
                break
    
    return wszystkie_dlugosci_komentarzy


def generuj_liczby_binarne(liczby):
    liczby_binarne = []

    for liczba in liczby:
        if liczba % 2 == 0:
            liczby_binarne.append(0)
        else:
            liczby_binarne.append(1)
    return liczby_binarne

def konwertuj_do_X_bitowych(liczby_bin,ile_bitow):
    liczby_X_bitowe = []
    aktualna_liczba = 0

    while len(liczby_bin) >= ile_bitow:############################################################################################### 4/8
        aktualna_partia = liczby_bin[:ile_bitow]###################################################################################### 4/8
        aktualna_liczba = 0

        for bit in aktualna_partia:
            aktualna_liczba = (aktualna_liczba << 1) | bit

        liczby_X_bitowe.append(aktualna_liczba)
        liczby_bin = liczby_bin[ile_bitow:]########################################################################################### 4/8

    return bytearray(liczby_X_bitowe)

# Ustaw klucz API YouTube Data
api_key = 'AIzaSyA7eDRVuoOcMC8qBK2MKh43B4rhCv7xVZo'

# Identyfikatory filmów
video_ids = [
    '9P5FA3Em1P8',
    'gdZLi9oWNZg',
    'jNQXAC9IVRw',
    'WMweEpGlu_U',
    'XsX3ATc3FbA',
    'MBdVXkSdhwU',
    '9bZkp7q19f0',
    '-5q5mZbe3V8',
    'ioNng23DkIM',
    'kffacxfA7G4',
]

poprzedni_wynik = int(time.time() * 1000)

def generuj_wyniki(ile_ma_wygenerowac):
    poprzedni_wynik = int(time.time() * 1000)
    
    max_comments_per_video = (ile_ma_wygenerowac/10)*8

    lista_bajtow_do_klucza = []

    for video_id in video_ids:
        random.seed(poprzedni_wynik)  # Ustaw ziarno na poprzedni wynik lub czas systemowy w milisekundach
        dlugosci_komentarzy = pobierz_dlugosci_komentarzy(api_key, [video_id], max_comments_per_video)
        liczby_bin = generuj_liczby_binarne(dlugosci_komentarzy)
        liczby_8_bitowe = konwertuj_do_X_bitowych(liczby_bin,8)
        for liczba in liczby_8_bitowe:
            #if liczba != 0 and liczba != 255:######################################################################################################## 255/15
                #print(f"Film: {video_id} | Liczba 8-bitowa: {liczba}")############################################################################### 8/4
            lista_bajtow_do_klucza.append(liczba)
            # Oblicz nowy poprzedni wynik
            poprzedni_wynik = liczba
    return bytearray(lista_bajtow_do_klucza)

        
        
# Fun generująca wyniki
#arraybytenew = generuj_wyniki(100)
#for n in arraybytenew:
#    print(n)

