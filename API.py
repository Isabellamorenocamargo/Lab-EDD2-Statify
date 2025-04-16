import json
from dotenv import load_dotenv
import os
import requests

class API:

    def __init__(self):
        # Cargo las variables de entorno desde el .env
        load_dotenv()

        # Se obtienen las credenciales de API de Spotify desde las variables de entorno
        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")  
    
    # Función para obtener el token de acceso a la API de Spotify
    # Se utiliza el grant_type client_credentials para obtener el token
    # Se utiliza el client_id y client_secret para autenticar la aplicación
    # Se utiliza el endpoint /api/token para obtener el token
    # Se utiliza el método POST para enviar los datos al servidor
    # Se utiliza el header Content-Type para indicar el tipo de contenido que se está enviando
    # Se utiliza el data para enviar los datos al servidor
    # Se utiliza el método json() para obtener la respuesta en formato JSON
    def getAccessToken(self, client_id:str, client_secret:str):
        try:
                res = requests.post("https://accounts.spotify.com/api/token", 
                                    headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                    data={"grant_type": "client_credentials",
                                        "client_id": client_id,
                                        "client_secret": client_secret 
                                        })
                return res.json()['access_token']
        except Exception as e:
            print(e)

    # Función para extraer la parte del ID de la playlist
    def extractPlaylistId(self, spotifyUrl):
        # Pregunta si la URL contiene '/playlist/' y si es asi, la divide en dos partes y se queda con la segunda parte
        if '/playlist/' in spotifyUrl:
            parts = spotifyUrl.split('/playlist/')[1]
            # Pregunta si la URL contiene '?' y si es asi, la divide en dos partes y se queda con la primera parte
            if '?' in parts:
                parts = parts.split('?')[0]
                return parts
            # Si no contiene '?' retorna la parte obtenida en el primer if
            else:
                return parts
        # Si no contiene '/playlist/' significa que no es una URL valida
        else:
            return None

    def getPlayList(self, access_token: str, playlist_id):
        i = 0
        allResponses = []

        while True:
            try:
                result = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}&limit=100",
                                headers={"Authorization": f"Bearer {access_token}"})

                jsonResult = result.json()
                allResponses.append(jsonResult)
                i += 100
                if jsonResult['next'] is None or not jsonResult.get('next'):
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        return allResponses

    def startAPI(self, playlist:str):
        token = self.getAccessToken(self.clientId, self.clientSecret)
        playlistId = self.extractPlaylistId(playlist)
        jsonPlaylist = self.getPlayList(token, playlistId)
        with open('playlist.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(jsonPlaylist, jsonFile, ensure_ascii=False, indent=4)
