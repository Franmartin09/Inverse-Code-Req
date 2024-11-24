import os
import ast
from collections import defaultdict


class TreeNode:
    def __init__(self, func_name):
        self.func_name = func_name
        self.left = None
        self.right = None
        self.dependencies = set()

    def insert(self, func_name):
        if func_name < self.func_name:
            if self.left is None:
                self.left = TreeNode(func_name)
            else:
                self.left.insert(func_name)
        else:
            if self.right is None:
                self.right = TreeNode(func_name)
            else:
                self.right.insert(func_name)

    def add_dependency(self, dep_name):
        """Agrega dependencias al nodo."""
        self.dependencies.add(dep_name)

    def in_order_traversal(self, visited):
        """Recorrido en orden para visitar las funciones según su profundidad de dependencias."""
        chunks = []
        # Recorrer subárbol izquierdo
        if self.left:
            chunks.extend(self.left.in_order_traversal(visited))
        # Procesar nodo actual si no se ha visitado
        if self.func_name not in visited:
            visited.add(self.func_name)
            chunks.append(self.func_name)
        # Recorrer subárbol derecho
        if self.right:
            chunks.extend(self.right.in_order_traversal(visited))
        return chunks


def extract_code_elements(file_path):
    """
    Extrae clases, funciones y dependencias de cualquier archivo Python.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    code_elements = {}  # Guarda nodos (clases y funciones)
    global_dependencies = set()  # Dependencias globales
    function_calls = defaultdict(set)  # Dependencias entre funciones y métodos

    class CodeVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node):
            code_elements[node.name] = node
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    method_name = f"{node.name}.{child.name}"

                    # Analizar dependencias en métodos
                    for subchild in ast.walk(child):
                        if isinstance(subchild, ast.Call):
                            self._add_call_dependency(method_name, subchild)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # Registrar funciones globales
            code_elements[node.name] = node

            # Analizar dependencias en funciones
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    self._add_call_dependency(node.name, child)
            self.generic_visit(node)

        def visit_Expr(self, node):
            # Identificar expresiones globales con llamadas
            if isinstance(node.value, ast.Call):
                self._add_global_dependency(node.value)
            self.generic_visit(node)

        def visit_Import(self, node):
            # Registrar imports como dependencias globales
            for alias in node.names:
                global_dependencies.add(alias.name)
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            # Registrar imports como dependencias globales
            module = node.module if node.module else ""
            for alias in node.names:
                global_dependencies.add(f"{module}.{alias.name}")
            self.generic_visit(node)

        def _add_call_dependency(self, source, call_node):
            """Añade dependencias entre funciones, métodos o llamadas globales."""
            if isinstance(call_node.func, ast.Name):  # Llamada directa (e.g., foo())
                function_calls[source].add(call_node.func.id)
            elif isinstance(call_node.func, ast.Attribute):  # Llamada a atributo (e.g., obj.method())
                if isinstance(call_node.func.value, ast.Name):
                    function_calls[source].add(call_node.func.attr)

        def _add_global_dependency(self, call_node):
            """Registra dependencias desde el contexto global."""
            if isinstance(call_node.func, ast.Name):
                global_dependencies.add(call_node.func.id)
            elif isinstance(call_node.func, ast.Attribute):
                global_dependencies.add(call_node.func.attr)

    visitor = CodeVisitor()
    visitor.visit(tree)

    return code_elements, function_calls, global_dependencies


def create_chunks(file_path):
    """
    Crea chunks de código respetando las dependencias entre clases, funciones y código global.
    """
    code_elements, function_calls, global_dependencies = extract_code_elements(file_path)

    # Crear el árbol BST con las dependencias
    root = None
    function_nodes = {}

    # Insertar funciones en el árbol binario de búsqueda
    for func, dependencies in function_calls.items():
        if func not in function_nodes:
            function_nodes[func] = TreeNode(func)
        for dep in dependencies:
            if dep not in function_nodes:
                function_nodes[dep] = TreeNode(dep)
            function_nodes[func].add_dependency(dep)

    # Insertar en el árbol
    for node in function_nodes.values():
        if root is None:
            root = node
        else:
            root.insert(node.func_name)

    # Realizar recorrido en profundidad (DFS) sobre el árbol
    visited = set()
    sorted_functions = root.in_order_traversal(visited)

    # Crear los chunks
    chunks = []
    used_elements = set()  # Evita duplicados

    # Procesar funciones con dependencias
    for func in sorted_functions:
        if func not in used_elements:
            used_elements.add(func)
            if func in code_elements:
                chunk_code = ast.unparse(code_elements[func])
                # Añadir dependencias en el chunk, si es necesario
                dependencies_code = []
                for dep in function_calls.get(func, []):
                    if dep in code_elements and dep not in used_elements:
                        dependencies_code.append(ast.unparse(code_elements[dep]))
                        used_elements.add(dep)
                # Combinar dependencias con la función
                chunks.append("\n\n".join(dependencies_code + [chunk_code]))

    # Procesar funciones sin dependencias (no aparecen en function_calls)
    for func, func_node in code_elements.items():
        if func not in used_elements and func not in function_calls:
            used_elements.add(func)
            chunk_code = ast.unparse(func_node)
            chunks.append(chunk_code)

    # Agregar dependencias globales al primer chunk si no se usaron
    if global_dependencies:
        global_code = "\n".join(f"# Global dependency: {dep}" for dep in global_dependencies)
        if chunks:
            chunks[0] = f"{global_code}\n\n{chunks[0]}"
        else:
            chunks.append(global_code)

    return chunks



def generate_chunks(directory):
    """
    Genera chunks de código para todos los archivos Python en el directorio.
    """
    chunks = []
    used_functions = set()  # Para realizar depuración y evitar duplicados entre archivos.

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Procesando archivo: {file_path}")
                file_chunks = create_chunks(file_path)

                # Revisar y depurar para eliminar duplicados entre archivos
                new_chunks = []
                for chunk in file_chunks:
                    functions_in_chunk = {
                        line.split(" ")[-1] for line in chunk.split("\n") if "def " in line
                    }

                    if not functions_in_chunk.intersection(used_functions):
                        used_functions.update(functions_in_chunk)
                        new_chunks.append(chunk)

                chunks.extend(new_chunks)

    return chunks


# if __name__ == "__main__":
#     code_directory = "code"
#     output_dir = "chunks_output"
#     os.makedirs(output_dir, exist_ok=True)

#     # Generar chunks
#     code_chunks = generate_chunks(code_directory)
    
#     # Guardar chunks
#     for i, chunk in enumerate(code_chunks):
#         with open(os.path.join(output_dir, f"chunk_{i+1}.py"), "w", encoding="utf-8") as chunk_file:
#             chunk_file.write(chunk)

#     print(f"Se generaron {len(code_chunks)} chunks en el directorio '{output_dir}'")
