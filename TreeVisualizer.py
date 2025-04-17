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
    # Añadir nodos
    def _add_nodes_edges(self, node):
        if node is None:
            return

        node_id = str(node.uniqueID) # Id unico

        label = f"{(node.name)}"

        # Comentario sobre los nodos al hacer "Hover"
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
        self._add_nodes_edges(self.tree.root)

        # Genera el SVG como string
        svg_content = self.dot.pipe(format='svg').decode('utf-8')

        # Inserta CSS y JS
        svg_content = self.incrustar_estilos_y_scripts(svg_content)

        # Guarda el SVG personalizado
        with open(filename + '.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)

        print(f"Árbol AVL guardado como {filename}.svg")


    # Personalización de los árboles a través de CSS y JS 
    def incrustar_estilos_y_scripts(self, svg):
        # CSS embebido
        estilo = """
        <style type="text/css">
            text {
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
            }
            .node:hover polygon{
            stroke: black;
            stroke-width: 2;
            fill: #d0e1ff;
            }
            .edge path {
                stroke-width: 3;
            }
        </style>
        """

        # JS
        script = """
        <script type="text/javascript">
        document.addEventListener("DOMContentLoaded", function() {
            const svg = document.querySelector("svg");
            svg.style.transform = "scale(0.5)";
            svg.style.transformOrigin = "top left";
        });
        </script>
        """

        # Insertar nuevamente en el SVG
        insert_index = svg.rfind("</svg>")
        return svg[:insert_index] + estilo + script + svg[insert_index:]
