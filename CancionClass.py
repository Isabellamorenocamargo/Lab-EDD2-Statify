class Cancion:
    
    def __init__(self, uniqueID: int, name: str, artists: list, duracion: int, popularidad: int):
        self.uniqueID = uniqueID
        self.name = name
        self.artists = artists
        self.duracion = duracion  # En segundos
        self.popularidad = popularidad  # De 0 a 100
        self.left = None
        self.right = None
        self.balance = 0

    def __str__(self):
        return f"{self.name} - Popularidad: {self.popularidad}"
