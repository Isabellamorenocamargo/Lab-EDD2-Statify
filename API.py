import json
from dotenv import load_dotenv
import os
import requests

class API:
    """
    Clase que permite interactuar con la API de Spotify para obtener información 
    sobre playlists, incluyendo pistas e imágenes.
    """

    def __init__(self):
        """
        Constructor de la clase API.
        Carga las variables de entorno necesarias para la autenticación.
        """
        load_dotenv()
        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")  
    
    def getAccessToken(self, client_id: str, client_secret: str) -> str:
        """
        Solicita un token de acceso a la API de Spotify usando las credenciales proporcionadas.

        @param client_id: ID del cliente de Spotify.
        @param client_secret: Clave secreta del cliente de Spotify.
        @return: Token de acceso como string.
        """
        try:
            res = requests.post(
                "https://accounts.spotify.com/api/token", 
                headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret 
                }
            )
            return res.json()['access_token']
        except Exception as e:
            print(e)

    def extractPlaylistId(self, spotifyUrl: str) -> str:
        """
        Extrae el ID de la playlist desde una URL de Spotify.

        @param spotifyUrl: URL completa de la playlist de Spotify.
        @return: ID de la playlist como string.
        """
        if '/playlist/' in spotifyUrl:
            # Si la URL contiene "/playlist/", separamos para obtener el ID y tomamos la parte después de "/playlist/"
            parts = spotifyUrl.split('/playlist/')[1] 
            
            if '?' in parts:
                # Si hay parámetros al final de la URL (por ejemplo: ?si=abc...), los eliminamos y retornamos solo el ID limpio de la playlist
                parts = parts.split('?')[0]
                return parts
            else:
                return parts
        else:
            # Si no se encuentra "/playlist/" en la URL, asumimos que ya es solo el ID y lo retornamos
            return spotifyUrl

    def getPlayList(self, access_token: str, playlist_id: str) -> list:
        """
        Obtiene las pistas de una playlist de Spotify usando paginación.

        @param access_token: Token de acceso válido.
        @param playlist_id: ID de la playlist.
        @return: Lista de respuestas JSON con la información de las pistas.
        """
        i = 0
        allResponses = []

        while True:
            try:
                result = requests.get(
                    f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}&limit=100",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                jsonResult = result.json()
                allResponses.append(jsonResult)
                i += 100

                # Comprobamos si hay más resultados para paginar, si no hay más salimos del bucle
                if jsonResult['next'] is None or not jsonResult.get('next'):
                    break

            except Exception as e:
                break
        
        return allResponses

    def startAPI(self, playlist: str):
        """
        Inicia el proceso de conexión con la API, obtiene la información de la playlist
        y guarda ambos en archivos JSON locales.

        @param playlist: URL completa o ID de la playlist de Spotify.
        """
        token = self.getAccessToken(self.clientId, self.clientSecret)
        playlistId = self.extractPlaylistId(playlist)
        jsonPlaylist = self.getPlayList(token, playlistId)

        # Guarda la información de la playlist en un archivo JSON
        with open('playlist.json', 'w', encoding='utf-8') as jsonFile:
            json.dump(jsonPlaylist, jsonFile, ensure_ascii=False, indent=4)