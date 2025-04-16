import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import AVL
import Procedimientos
import ArtistClass
import json
import API
import webbrowser
from TreeVisualizer import AVLTreeVisualizer

class StatifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Statify - Análisis de Árboles AVL")
        self.geometry("800x700")
        self.api = API.API()
        self.process = Procedimientos.Process()
        # Inicializamos los árboles (se recargan al cargar playlist)
        self.songsTree = AVL.AVLTree()
        self.artistsTree = AVL.AVLTree()
        self.popularityTree = AVL.AVLTree()
        
        self.create_widgets()
        self.inicializar_playlist()

    def create_widgets(self):
        # Frame superior para el título
        self.lbl_titulo = tk.Label(self, text="🎵 Statify - Análisis de Árboles AVL", font=("Helvetica", 20))
        self.lbl_titulo.pack(pady=10)

        # Frame para los botones de acción
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(pady=10)

        # Botones para cada acción
        btn_artista_canciones = tk.Button(self.frame_botones, text="Artista con más canciones", width=30,
                                          command=self.mostrar_artista_con_mas_canciones)
        btn_artista_canciones.grid(row=0, column=0, padx=5, pady=5)

        btn_artista_popular = tk.Button(self.frame_botones, text="Artista con mayor popularidad", width=30,
                                        command=self.mostrar_artista_mas_popular)
        btn_artista_popular.grid(row=0, column=1, padx=5, pady=5)

        btn_niveles_artista = tk.Button(self.frame_botones, text="Niveles del artista más popular", width=30,
                                        command=self.mostrar_niveles_artista)
        btn_niveles_artista.grid(row=1, column=0, padx=5, pady=5)

        btn_alturas_arboles = tk.Button(self.frame_botones, text="Alturas de los árboles", width=30,
                                        command=self.mostrar_alturas)
        btn_alturas_arboles.grid(row=1, column=1, padx=5, pady=5)

        btn_rotaciones = tk.Button(self.frame_botones, text="Número de rotaciones (canciones)", width=30,
                                   command=self.mostrar_rotaciones)
        btn_rotaciones.grid(row=2, column=0, padx=5, pady=5)

        btn_duracion_promedio = tk.Button(self.frame_botones, text="Canciones con duración > promedio", width=30,
                                          command=self.mostrar_canciones_mayor_duracion)
        btn_duracion_promedio.grid(row=2, column=1, padx=5, pady=5)

        btn_buscar_artista = tk.Button(self.frame_botones, text="Buscar canciones por artista", width=30,
                                       command=self.buscar_canciones_artista)
        btn_buscar_artista.grid(row=3, column=0, padx=5, pady=5)

        btn_top_canciones = tk.Button(self.frame_botones, text="Top N canciones populares", width=30,
                                      command=self.mostrar_top_n_canciones)
        btn_top_canciones.grid(row=3, column=1, padx=5, pady=5)

        btn_visualizar_arbol = tk.Button(self.frame_botones, text="Visualizar árboles (SVG)", width=30,
                                         command=self.visualizar_arbol)
        btn_visualizar_arbol.grid(row=4, column=0, padx=5, pady=5)

        btn_nueva_playlist = tk.Button(self.frame_botones, text="Consultar otra playlist", width=30,
                                       command=self.consultar_nueva_playlist)
        btn_nueva_playlist.grid(row=4, column=1, padx=5, pady=5)

        btn_salir = tk.Button(self, text="Salir", width=20, command=self.quit)
        btn_salir.pack(pady=10)

        # Área de salida (Text widget) para mostrar resultados dentro de la interfaz.
        self.text_output = tk.Text(self, height=10, width=90, wrap="word")
        self.text_output.pack(pady=10)
        self.text_output.configure(state="disabled")  # Hacemos que no sea editable

    def clear_text(self):
        self.text_output.configure(state="normal")
        self.text_output.delete('1.0', tk.END)
        self.text_output.configure(state="disabled")

    def append_text(self, text):
        self.text_output.configure(state="normal")
        self.text_output.insert(tk.END, text + "\n")
        self.text_output.see(tk.END)
        self.text_output.configure(state="disabled")

    def inicializar_playlist(self):
        # Preguntar al usuario si quiere usar una playlist nueva o la predeterminada
        use_nueva = messagebox.askquestion("Playlist", "¿Desea usar una playlist nueva?")
        if use_nueva == 'yes':
            playlist = simpledialog.askstring("Playlist", "Inserte la URL de su playlist:")
            if playlist and "open.spotify.com/playlist/" in playlist:
                self.playlist = playlist.strip()
            else:
                messagebox.showerror("Error", "URL no válida. Se usará la predeterminada.")
                self.playlist = "https://open.spotify.com/playlist/3sWwKAETNrcp41VnrfKeT1?si=OYwNXh0fRrGYMuIAS5kODA"
        else:
            self.playlist = "https://open.spotify.com/playlist/3sWwKAETNrcp41VnrfKeT1?si=OYwNXh0fRrGYMuIAS5kODA"
        self.cargar_playlist()

    def cargar_playlist(self):
        # Llama a la API para descargar la playlist y genera los árboles
        self.api.startAPI(self.playlist)
        try:
            with open('playlist.json', 'r', encoding='utf-8') as jsonFile:
                jsonPlaylist = json.load(jsonFile)
        except Exception as e:
            self.clear_text()
            self.append_text(f"Error al cargar playlist.json:\n{e}")
            return

        # Reinicializamos los árboles
        self.songsTree = AVL.AVLTree()
        self.artistsTree = AVL.AVLTree()
        self.popularityTree = AVL.AVLTree()
        artistas_unicos = {}

        for i in range(len(jsonPlaylist)):
            for j in range(len(jsonPlaylist[i]['items'])):
                track_info = jsonPlaylist[i]['items'][j]['track']
                if not track_info:
                    continue
                artistList = []
                for k in range(len(track_info['artists'])):
                    artist = track_info['artists'][k]['name']
                    artistID = track_info['artists'][k]['id']
                    if artist not in artistas_unicos:
                        artistas_unicos[artist] = ArtistClass.Artist(self.artistsTree.convertAscii(artistID), artist)
                    artistList.append(artistas_unicos[artist])
                    self.artistsTree.generateArtistsTree(artistas_unicos[artist])
                songID = track_info['id']
                songName = track_info['name']
                songDuration = track_info['duration_ms']
                songPopularity = track_info['popularity']
                self.songsTree.generateSongsTree(self.songsTree.convertAscii(songID), songName,
                                                  artistList, songDuration, songPopularity, self.popularityTree)
        self.clear_text()
        self.append_text("La playlist se ha cargado correctamente.")

    # Funciones para cada opción, ahora limpiando el área de salida antes de mostrar resultados
    def mostrar_artista_con_mas_canciones(self):
        self.clear_text()
        artista = self.process.artista_con_mas_canciones(self.songsTree)
        self.append_text(f"Artista con más canciones:\n{artista}")

    def mostrar_artista_mas_popular(self):
        self.clear_text()
        artista = self.process.artista_mas_popular(self.songsTree)
        self.append_text(f"Artista con mayor popularidad:\n{artista}")

    def mostrar_niveles_artista(self):
        self.clear_text()
        artista = self.process.artista_mas_popular(self.songsTree)
        niveles = self.process.mostrar_niveles_mayor_popularidad(self.songsTree)
        self.append_text(f"Niveles del artista más popular ({artista}):\n{niveles}")

    def mostrar_alturas(self):
        self.clear_text()
        alturaSongs, alturaArtists = self.process.alturas(self.songsTree, self.artistsTree)
        self.append_text(f"Altura del árbol de canciones: {alturaSongs}\nAltura del árbol de artistas: {alturaArtists}")

    def mostrar_rotaciones(self):
        self.clear_text()
        rotaciones = self.process.rotacionesSongs(self.songsTree)
        self.append_text(f"Número de rotaciones en el árbol de canciones: {rotaciones}")

    def mostrar_canciones_mayor_duracion(self):
        self.clear_text()
        canciones = self.process.cancionesConDuracionMayorAlPromedio(self.songsTree.root)
        self.append_text("Canciones con duración mayor al promedio:")
        self.append_text(str(canciones))

    def buscar_canciones_artista(self):
        self.clear_text()
        nombre = simpledialog.askstring("Buscar Canciones", "Ingrese el nombre del artista:")
        if nombre:
            canciones = self.process.canciones_artista(self.songsTree, self.artistsTree, nombre.strip())
            if canciones:
                self.append_text(f"Canciones de {nombre}:\n{canciones}")
            else:
                self.append_text(f"No se encontraron canciones para {nombre}.")

    def mostrar_top_n_canciones(self):
        self.clear_text()
        n_str = simpledialog.askstring("Top N Canciones", "Ingrese la cantidad de canciones populares a mostrar:")
        try:
            n = int(n_str)
            if n <= 0:
                self.append_text("Ingrese un número mayor a cero.")
                return
        except Exception:
            self.append_text("Debe ingresar un número válido.")
            return
        canciones = self.process.obtener_n_canciones_populares(self.popularityTree, n)
        self.append_text(f"Top {n} canciones más populares:\n{canciones}")

    def visualizar_arbol(self):
        self.clear_text()
        opcion = simpledialog.askstring("Visualizar Árbol",
                                        "Seleccione el árbol a visualizar:\n1. Artistas\n2. Canciones\n3. Canciones por popularidad")
        if not opcion:
            return
        opcion = opcion.strip()
        if opcion == '1':
            AVLTreeVisualizer(self.artistsTree, False, False).render("AVL_artists")
            webbrowser.open("AVL_artists.svg")
            self.append_text("Árbol de artistas generado y abierto en el navegador.")
        elif opcion == '2':
            AVLTreeVisualizer(self.songsTree, True, True).render("AVL_songs")
            webbrowser.open("AVL_songs.svg")
            self.append_text("Árbol de canciones generado y abierto en el navegador.")
        elif opcion == '3':
            AVLTreeVisualizer(self.popularityTree, True, True).render("AVL_popularity")
            webbrowser.open("AVL_popularity.svg")
            self.append_text("Árbol de canciones por popularidad generado y abierto en el navegador.")
        else:
            self.append_text("Opción no válida para visualizar árbol.")

    def consultar_nueva_playlist(self):
        self.clear_text()
        use_nueva = messagebox.askquestion("Nueva Playlist", "¿Desea usar una playlist nueva?")
        if use_nueva == 'yes':
            playlist = simpledialog.askstring("Playlist", "Inserte la URL de su playlist:")
            if playlist and "open.spotify.com/playlist/" in playlist:
                self.playlist = playlist.strip()
            else:
                self.append_text("URL no válida. Se usará la anterior.")
        self.cargar_playlist()

if __name__ == "__main__":
    app = StatifyApp()
    app.mainloop()
