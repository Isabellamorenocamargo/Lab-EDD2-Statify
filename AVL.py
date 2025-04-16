import CancionClass
import ArtistClass
import json
class AVLTree:
    def __init__(self):
        self.root = None
        self.rotaciones = 0

    def getRotaciones(self):
        return self.rotaciones

    def addNode(self, root, new_node):
        """
        Agrega un nuevo nodo al árbol AVL y realiza las rotaciones necesarias para mantener el balance.
        
        Parámetros:
        - root: Nodo raíz del árbol (o subárbol) actual.
        - new_node: Nuevo nodo a insertar en el árbol.
        
        Retorna:
        - La nueva raíz del subárbol después de la inserción y posibles rotaciones.
        """
        if root is None:
            return new_node
        
        if root.uniqueID == new_node.uniqueID:
            return root
        
        if new_node.uniqueID > root.uniqueID:
            root.right = self.addNode(root.right, new_node)
        else:
            root.left = self.addNode(root.left, new_node)
        
        root.balance = self.height(root.left) - self.height(root.right)
        
        if root.balance == 2:
            self.rotaciones += 1
            if root.left.balance == -1:
                self.rotaciones += 1
                root.left = self.rotate_right(root.left)
            return self.rotate_left(root)
        
        if root.balance == -2:
            self.rotaciones += 1
            if root.right.balance == 1:
                self.rotaciones += 1
                root.right = self.rotate_left(root.right)
            return self.rotate_right(root)
        
        return root
    
    def addNodePopularity(self, root, new_node):
        if root is None:
            return new_node
        
        if root.popularidad == new_node.popularidad and root.uniqueID == new_node.uniqueID:
            return root
        
        if new_node.popularidad > root.popularidad:
            root.right = self.addNodePopularity(root.right, new_node)
        elif new_node.popularidad < root.popularidad:
            root.left = self.addNodePopularity(root.left, new_node)
        else:
            # Si la popularidad es igual, se utiliza el uniqueID como criterio de desempate.
            if new_node.uniqueID > root.uniqueID:
                root.right = self.addNodePopularity(root.right, new_node)
            else:
                root.left = self.addNodePopularity(root.left, new_node)
        
        root.balance = self.height(root.left) - self.height(root.right)
        
        if root.balance == 2:
            self.rotaciones += 1
            if root.left.balance == -1:
                self.rotaciones += 1
                root.left = self.rotate_right(root.left)
            return self.rotate_left(root)
        
        if root.balance == -2:
            self.rotaciones += 1
            if root.right.balance == 1:
                self.rotaciones += 1
                root.right = self.rotate_left(root.right)
            return self.rotate_right(root)
        
        return root
    
    def rotate_right(self, node):
        aux = node.right
        node.right = aux.left
        aux.left = node
        aux.balance = self.height(aux.left) - self.height(aux.right)
        node.balance = self.height(node.left) - self.height(node.right)
        return aux
    
    def rotate_left(self, node):
        aux = node.left
        node.left = aux.right
        aux.right = node
        aux.balance = self.height(aux.left) - self.height(aux.right)
        node.balance = self.height(node.left) - self.height(node.right)
        return aux
    
    def height(self, node):
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))
    
    def pre_order(self, node):
        if node is not None:
            print(node)
            self.pre_order(node.left)
            self.pre_order(node.right)
    
    def generateSongsTree(self, id, name, artistas, duracion, popularidad, popularityTree):
        new_node = CancionClass.Cancion(id, name, artistas, duracion, popularidad)
        new_node_popularity = CancionClass.Cancion(id, name, artistas, duracion, popularidad)

        # Agregar canción al árbol
        if self.root is None:
            self.root = new_node
            popularityTree.root = new_node_popularity
        else:
            self.root = self.addNode(self.root, new_node)  
            popularityTree.root = popularityTree.addNodePopularity(popularityTree.root, new_node_popularity)  

    def generateArtistsTree(self, artist):
        if self.root is None:
            self.root = artist
        else:
            self.root = self.addNode(self.root, artist)

    def search(self, node, target):
        if node is None:
            return None
        elif node.uniqueID == target.uniqueID:  # Compara por valor, no por referencia
            return node
        elif target.uniqueID < node.uniqueID:
            return self.search(node.left, target)
        else:
            return self.search(node.right, target)
        
    def searchByName(self, node, name):
        if node is None:
            return None
        elif node.name == name:  # Compara por valor, no por referencia
            return node
        
        left_result = self.searchByName(node.left, name)
        if left_result:
            return left_result
        return self.searchByName(node.right, name)
    
    def convertAscii(self, string):
        ascii = ""
        # Se carga el archivo JSON que contiene los valores en ASCII de cada letra
        with open('asciiTable.json', 'r', encoding='utf-8') as file:
            asciiFile = json.load(file)
        # Se recorre el string, se obtiene el valor de cada letra en ascii y se concatena a un string
        for i in range(len(string)):
            numero = int(asciiFile[string[i]])
            ascii += str(numero)

        # Se convierte el string en un numero entero y se retorna como id
        numAscii = int(ascii)
        return numAscii
