from AVL import AVLTree
from ArtistClass import Artist

class Process:
    #PUNTO 1 = ¿Qué artista tiene mayor número de canciones en la playlist?
    #Contador es un diccionario
    def contar_canciones_por_artista(self, songsTree, songsTreeRoot, contador):
        """
        Recorre el árbol de canciones y cuenta cuántas veces aparece cada artista en la playlist.

        Parámetros:
        - songsTree: Árbol AVL de canciones.
        - songsTreeRoot: Nodo raíz del árbol de canciones.
        - contador: Diccionario donde se almacena la cantidad de canciones por artista.
        """
        if songsTreeRoot is None:
            return
        
        # Recorre los artistas por cada canción
        for artist in songsTreeRoot.artists:
                if artist in contador:
                    contador[artist] += 1 #Si ya está en el diccionario este artista, le suma 1
                else:
                    contador[artist] = 1 #Si no está en el diccionario, lo pone con valor incial 1
        
        self.contar_canciones_por_artista(songsTree, songsTreeRoot.left, contador)
        self.contar_canciones_por_artista(songsTree, songsTreeRoot.right, contador)

    def artista_con_mas_canciones(self, songsTree):
        """
        Determina qué artista tiene más canciones registradas en la playlist.
        
        Parámetros:
        - songsTree: Árbol AVL de canciones.
        """
        contador = {}
        self.contar_canciones_por_artista(songsTree, songsTree.root, contador)
        
        if not contador:
            return None  # Si el árbol está vacío
        
        return max(contador, key=contador.get)

    #Punto 2 = ¿Qué artista tiene mayor índice de popularidad? (Suma de popularidades de las canciones del artista)
    def contar_popularidad_artistas(self, songsTree, songsTreeRoot, contador):
        """
        Recorre el árbol de canciones y suma el índice de popularidad total por artista
        
        Parámetros:
        - songsTree: Árbol AVL que contiene las canciones.
        - songsTreeRoot: Nodo raíz del árbol de canciones.
        - contador: Diccionario que almacena la suma de popularidad de cada artista.
        """
        if songsTreeRoot is None:
            return contador

        # Recorre los artistas por cada canción
        for artist in songsTreeRoot.artists:
                if artist in contador:
                    contador[artist] += songsTreeRoot.popularidad  # Si el artista ya existe, sumamos la popularidad de esta cancion
                else:
                    contador[artist] = songsTreeRoot.popularidad  # Si no existe, lo agregamos con su popularidad

        self.contar_popularidad_artistas(songsTree, songsTreeRoot.left, contador)
        self.contar_popularidad_artistas(songsTree, songsTreeRoot.right, contador)

    def artista_mas_popular(self, songsTree):
        """
        Busca el artista con mayor popularidad acumulada sumando la popularidad de todas sus canciones.
        
        Parámetros:
        - songsTree: Árbol AVL de canciones.
        """
        contador = {}
        self.contar_popularidad_artistas(songsTree, songsTree.root, contador)

        if not contador:
            return None

        # Encontramos el artista con mayor popularidad
        return max(contador, key=contador.get)
    
    #Punto 3 = ¿En qué niveles del árbol AVL se encuentran las canciones del artista con mayor popularidad?
    def buscar_niveles(self, songsTree, songsTreeRoot, contador, artistMayor, c):
        """
        Recorre recursivamente el árbol AVL de canciones para identificar en qué niveles se encuentran las canciones
        del artista con mayor popularidad.

        Parámetros:
        - songsTree: Árbol AVL de canciones.
        - songsTreeRoot: Nodo raíz actual del árbol de canciones.
        - contador: Diccionario que almacena la cantidad de canciones por nivel.
        - artistMayor: Artista identificado con mayor popularidad.
        - c: Contador de niveles (profundidad actual en el árbol).

        Retorna:
        - El diccionario 'contador' actualizado con los niveles y la cantidad de canciones del artista.
        """
        if songsTreeRoot is None:
            return contador

        c = c + 1
        nivel = "Nivel " + str(c)
        for artist in songsTreeRoot.artists:
            if artist == artistMayor:
                if nivel in contador:
                    contador[nivel] += 1  # Si hay otra canción en el mismo nivel se suma 1
                else:
                    contador[nivel] = 1  # Si el nivel de la canción aún no está en el contador se añade

        self.buscar_niveles(songsTree, songsTreeRoot.left, contador, artistMayor, c)
        self.buscar_niveles(songsTree, songsTreeRoot.right, contador, artistMayor, c)

    def mostrar_niveles_mayor_popularidad(self, songsTree):
        """
        Determina y muestra los niveles del árbol AVL en los que se encuentran las canciones del artista con mayor popularidad.

        Parámetros:
        - songsTree: Árbol AVL de canciones.
        - artistsTree: Árbol AVL de artistas.

        Retorna:
        - Una cadena con los niveles identificados separados por comas, o None si no se encuentran coincidencias.
        """
        artistMayor = self.artista_mas_popular(songsTree) # Se obtiene el artista con mayor popularidad acumulada
        contador = {} # Diccionario para almacenar la cantidad de canciones por nivel
        c = 0
        self.buscar_niveles(songsTree, songsTree.root, contador, artistMayor, c)
        if not contador:
            return None # Retorna None si no se encontraron canciones del artista en el árbol
        niveles = ""
        for nivel in contador:
            niveles = niveles + ", " + nivel # Concatena los niveles encontrados en una cadena separados por comas

        return niveles
    
    #Punto 4 = ¿Cuál es la altura del árbol AVL de canciones? ¿Y del árbol AVL de artistas?
    def alturas(self, songsTree, artistsTree):
        """
        Retorna la altura del árbol AVL de canciones y del árbol AVL de artistas.

        Parámetros:
        - songsTree: Árbol AVL que contiene las canciones.
        - artistsTree: Árbol AVL que contiene los artistas.

        Retorna:
        - Una tupla (altura_canciones, altura_artistas) que representa la altura del árbol de
        canciones y la altura del árbol de artistas, respectivamente.
        """
        return songsTree.height(songsTree.root), artistsTree.height(artistsTree.root)
    
    #Punto 5 = ¿Cuántas rotaciones fueron necesarias para balancear el árbol AVL de canciones durante su construcción?
    def rotacionesSongs(self, songsTree):
        """
        Retorna la cantidad total de rotaciones realizadas para balancear el árbol AVL de canciones.
        
        Parámetros:
        - songsTree: Árbol AVL que contiene las canciones, en el cual durante su construcción se han
                    actualizado internamente las rotaciones efectuadas.
        
        Retorna:
        - Un entero que representa la cantidad total de rotaciones simples ejecutadas.
        (Se consideran las rotaciones dobles como dos rotaciones simples).
        """
        return songsTree.getRotaciones()
    
    #Punto 6 = ¿Qué canciones tienen una duración superior al promedio de duración de todas las canciones en la playlist?
    def recorridoAcumulacion(self, songsTreeRoot):
        """
        Recorre de forma recursiva el árbol AVL de canciones para calcular la suma total de duraciones y el total de canciones.

        Parámetros:
        - songsTreeRoot: Nodo actual del árbol de canciones.

        Retorna:
        - Una tupla (sumaTotal, cantTotal) con la suma acumulada de duraciones y la cantidad de canciones.
        """
        if songsTreeRoot is None:
            return (0, 0)
        sumaIzq, cantIzq = self.recorridoAcumulacion(songsTreeRoot.left)
        sumaDer, cantDer = self.recorridoAcumulacion(songsTreeRoot.right)

        sumaTotal = songsTreeRoot.duracion + sumaIzq + sumaDer
        cantTotal = 1 + cantIzq + cantDer
        return (sumaTotal, cantTotal)
    
    def buscarCancionesConDuracionMayor(self, songsTreeRoot, promedio, lista_canciones):
        """
        Realiza un recorrido inorden del árbol AVL de canciones y añade a una lista aquellas canciones
        cuya duración es mayor al promedio.

        Parámetros:
        - songsTreeRoot: Nodo actual del árbol de canciones.
        - promedio: Valor promedio de duración de todas las canciones.
        - lista_canciones: Lista donde se almacenan los nombres de canciones que cumplen la condición.
        """
        if songsTreeRoot is None:
            return
        
        self.buscarCancionesConDuracionMayor(songsTreeRoot.left, promedio, lista_canciones)
        # Si la duración de la canción actual es mayor que el promedio, se añade su nombre a la lista
        if songsTreeRoot.duracion > promedio:
            lista_canciones.append(songsTreeRoot.name)
        self.buscarCancionesConDuracionMayor(songsTreeRoot.right, promedio, lista_canciones)
    
    def cancionesConDuracionMayorAlPromedio(self, songsTreeRoot):
        """
        Determina y retorna las canciones cuya duración es superior al promedio de todas las canciones de la playlist.
        
        Parámetros:
        - songsTreeRoot: Nodo raíz del árbol AVL de canciones.
        
        Retorna:
        - Una cadena con los nombres de las canciones que superan el promedio de duración, separados por comas.
        Retorna una lista vacía si el árbol está vacío.
        """
        suma, cantidad = self.recorridoAcumulacion(songsTreeRoot)
        if cantidad == 0:
            return []  # Evitar división por cero si el árbol está vacío.
        
        promedio = suma / cantidad

        lista_canciones = []  # Lista para almacenar las canciones que cumplen la condición
        self.buscarCancionesConDuracionMayor(songsTreeRoot, promedio, lista_canciones)
        songs = "" # Se concatenan los nombres de las canciones en una cadena
        for cancion in lista_canciones:
            songs = songs + ", " + str(cancion)
        return songs
    
    #Punto 7 = ¿Cuál es la complejidad temporal de buscar todas las canciones de un artista específico usando la estructura implementada? Justifica tu respuesta.
    def canciones_un_artista(self, songsTree, songsTreeRoot, contador, artist1):
        """
        Recorre recursivamente el árbol AVL de canciones para buscar y acumular los nombres de aquellas canciones
        que contengan al artista especificado.
        
        Parámetros:
        - songsTree: Árbol AVL de canciones.
        - songsTreeRoot: Nodo actual del árbol de canciones.
        - contador: Lista que almacena los nombres de las canciones que cumplen la condición.
        - artist1: Nodo o identificador del artista buscado (obtenido previamente).
        
        Retorna:
        - Acumula en 'contador' los nombres de las canciones en las que se encuentra al artista.
        """
        if songsTreeRoot is None:
            return
        
        for artist in songsTreeRoot.artists:
            if artist == artist1:
                contador.append(songsTreeRoot.name)
        
        self.canciones_un_artista(songsTree, songsTreeRoot.left, contador, artist1)
        self.canciones_un_artista(songsTree, songsTreeRoot.right, contador, artist1)

    def canciones_artista(self, songsTree, artistsTree, artistName):
        """
        Busca y retorna una cadena con los nombres de todas las canciones en las que aparece el artista dado.

        Parámetros:
        - songsTree: Árbol AVL de canciones.
        - artistsTree: Árbol AVL de artistas.
        - artistName: Nombre del artista a buscar.

        Retorna:
        - Una cadena que contiene los nombres de las canciones encontradas, separados por comas.
        Si no se encuentra el artista o el árbol está vacío, retorna una cadena vacía.
        """
        contador = []
        artist = artistsTree.searchByName(artistsTree.root, artistName) #Busca el objeto que tenga el nombre del artista
        self.canciones_un_artista(songsTree, songsTree.root, contador, artist)

        if contador == None:
            return   # Si el árbol está vacío
        
        songs = ""
        for cancion in contador:
            songs = songs + ", " + str(cancion)
        return songs
    
    #Punto 9 = Implementa un algoritmo que permita obtener las N canciones más populares de la playlist en tiempo O(log(n) + N).
    def obtener_n_canciones_populares(self, arbol_popularidad, N: int):
        """
        Retorna una lista con las N canciones más populares.

        Como parámetros tiene el arbol de canciones organizado por popularidad y
        el número de canciones populares a buscar.

        La complejidad del algoritmo es O(log(n) + N).
        """
        resultado = []
        stack = [] # Pila auxiliar
        current = arbol_popularidad.root

        while (stack or current) and len(resultado) < N:
            # Mientras current no sea None, vamos siempre al subárbol derecho.
            if current:
                stack.append(current) # Nodos visitados
                current = current.right # Mayor popularidad
            else:
                # Cuando current es None, se saca el nodo en la cima de la pila
                current = stack.pop()
                resultado.append(current.name)
                # Luego se recorre el subárbol izquierdo
                current = current.left

        return resultado
