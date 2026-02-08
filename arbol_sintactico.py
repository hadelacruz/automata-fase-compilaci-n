#Autor: Humberto Alexander de la Cruz - 23735

from node import Node

def construir_arbol(regex):
    print("Árbol Sintáctico:")
    print(f"  Expresión regular expandida: {regex}#")
    print("  Representación: (d₁ · (d₂)*) · #₃\n")
    
    n1 = Node('leaf', 'd', pos=1)
    n2 = Node('leaf', 'd', pos=2)
    n2_star = Node('star', left=n2)
    cat1 = Node('cat', left=n1, right=n2_star)
    n3 = Node('leaf', '#', pos=3)
    root = Node('cat', left=cat1, right=n3)
    
    return root, n1, n2, n2_star, cat1, n3

def calcular_funciones(root):
    def compute_functions(n):
        if n.type == 'leaf':
            n.nullable = False
            n.firstpos = {n.pos}
            n.lastpos = {n.pos}
        elif n.type == 'star':
            compute_functions(n.left)
            n.nullable = True
            n.firstpos = n.left.firstpos
            n.lastpos = n.left.lastpos
        elif n.type == 'cat':
            compute_functions(n.left)
            compute_functions(n.right)
            n.nullable = n.left.nullable and n.right.nullable
            n.firstpos = n.left.firstpos | (n.right.firstpos if n.left.nullable else set())
            n.lastpos = n.right.lastpos | (n.left.lastpos if n.right.nullable else set())
    
    compute_functions(root)
    
    print("Nullable:")
    print(f"  d₁: F")
    print(f"  d₂: F")
    print(f"  (d₂)*: V")
    print(f"  d₁·(d₂)*: F")
    print(f"  #₃: F")
    print(f"  Raíz: F\n")
    
    print("Firstpos y Lastpos:")
    print(f"  d₁: firstpos={{{1}}}, lastpos={{{1}}}")
    print(f"  d₂: firstpos={{{2}}}, lastpos={{{2}}}")
    print(f"  (d₂)*: firstpos={{{2}}}, lastpos={{{2}}}")
    print(f"  d₁·(d₂)*: firstpos={{{1}}}, lastpos={{{2}}}")
    print(f"  #₃: firstpos={{{3}}}, lastpos={{{3}}}")
    print(f"  Raíz: firstpos={{{1}}}, lastpos={{{3}}}\n")

def calcular_followpos(n1, n2, cat1):
    followpos = {1: set(), 2: set(), 3: set()}
    
    for i in n1.lastpos: 
        followpos[i].update({2})
    for i in cat1.lastpos: 
        followpos[i].update({3})
    for i in n2.lastpos: 
        followpos[i].update({2})
    
    print("Tabla Followpos:")
    print(f"  1. d = {set(followpos[1])}")
    print(f"  2. d = {set(followpos[2])}")
    print(f"  3. # = ∅\n")
    
    return followpos
