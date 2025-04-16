from graphviz import Digraph

class AVLTreeVisualizer:
    # Funcion constructor
    def __init__(self, avl_tree, mostrar_tooltip=True, es_arbol_artistas=False):
        self.tree = avl_tree # Objeto de tipo arbol AVL 
        self.dot = Digraph() # Herramienta para definir nodos y aristas en un grafico 

        self.mostrar_tooltip = mostrar_tooltip
        self.es_arbol_artistas = es_arbol_artistas

        # Personalización global del gráfico
        self.dot.attr(
            bgcolor='lightgrey', 
            label='Árbol AVL Visualizado', 
            fontsize='20', 
            fontname='Helvetica',
            rankdir='TB',         # De arriba hacia abajo
            ranksep='1.8',        # Separación vertical entre nodos
            nodesep='1.5'         # Separación horizontal entre nodos
            )

    def _add_nodes_edges(self, node):
        if node is None:
            return

        node_id = str(node.uniqueID) # Id unico

        label = f"{(node.name)}"

        tooltip = ""
        if self.mostrar_tooltip and self.es_arbol_artistas:
            tooltip = f"Duración: {round(node.duracion / 60000, 2)} minutos\nPopularidad: {node.popularidad}" # Mensaje al hacer hover sobre un nodos
        else:
            tooltip = f"ID: {node.uniqueID}"

        # Personalización del nodo
        self.dot.node(
            name=node_id,
            label=label,
            shape='box',         # Forma del nodo
            style='filled',          # Estilo de relleno
            fillcolor='lightblue',   # Color de fondo
            fontcolor='black',       # Color del texto
            fontname='Arial',        # Tipo de letra
            fontsize='40',           # Tamaño de letra
            tooltip = tooltip,
            _attributes={'id': node_id, 'title': tooltip}
        )
        #Nodos ubicados a la izquierda de su padre
        if node.left:
            self.dot.edge(node_id, str(node.left.uniqueID), color='blue', penwidth='4')
            self._add_nodes_edges(node.left)

        # Nodos ubicados a la derecha de su padre
        if node.right:
            self.dot.edge(node_id, str(node.right.uniqueID), color='green', penwidth='4')
            self._add_nodes_edges(node.right)

    # Funcion renderizadora
    def render(self, filename="avl_tree_interactivo"):
        self._add_nodes_edges(self.tree.root) # Agrega los nodos enlazados a aristas al grafico
        self.dot.render(filename, format="svg", cleanup=True) # Generar una imagen PNG
        print(f"Árbol AVL guardado como {filename}.svg")