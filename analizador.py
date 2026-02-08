#Autor: Humberto Alexander de la Cruz - 23735

class Node:
    def __init__(self, type, value=None, left=None, right=None, pos=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
        self.pos = pos
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()

def build_logic_and_simulate():
    print("=== ANALIZADOR LÉXICO ===\n")

    # Expresiones regulares de los lexemas
    regex_keywords = "public|class|if|else|static|void"
    regex_numerics = "d d*"  # donde d = [0-9]
    
    print("Lexemas identificados:")
    print(f"  1. Keywords: {regex_keywords}")
    print(f"  2. Literales Numéricos: {regex_numerics} (d = [0-9])")
    print(f"\nLexema seleccionado: Literales Numéricos ({regex_numerics})\n")

    # CREACIÓN DEL AUTÓMATA - Se ejecuta en la inicialización del Scanner
    print("Árbol Sintáctico:")
    print(f"  Expresión regular expandida: {regex_numerics}#")
    print("  Representación: (d₁ · (d₂)*) · #₃\n")
    
    n1 = Node('leaf', 'd', pos=1)
    n2 = Node('leaf', 'd', pos=2)
    n2_star = Node('star', left=n2)
    cat1 = Node('cat', left=n1, right=n2_star)
    n3 = Node('leaf', '#', pos=3)
    root = Node('cat', left=cat1, right=n3)

    nodes = [n1, n2, n2_star, cat1, n3, root]
    
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

    followpos = {1: set(), 2: set(), 3: set()}
    
    for i in n1.lastpos: followpos[i].update(n2_star.firstpos)
    for i in cat1.lastpos: followpos[i].update(n3.firstpos)
    for i in n2.lastpos: followpos[i].update(n2.firstpos)

    print("Tabla Followpos:")
    print(f"  1. d = {set(followpos[1])}")
    print(f"  2. d = {set(followpos[2])}")
    print(f"  3. # = ∅\n")

    print("Construcción del DFA:")
    states = {}
    unmarked_states = [frozenset(root.firstpos)]
    states_map = {unmarked_states[0]: 'A'}
    dfa_transitions = {}
    
    while unmarked_states:
        current_set = unmarked_states.pop(0)
        state_name = states_map[current_set]
        
        next_set = set()
        for p in current_set:
            if p != 3:
                next_set.update(followpos[p])
        
        if next_set:
            next_set_frozen = frozenset(next_set)
            if next_set_frozen not in states_map:
                states_map[next_set_frozen] = chr(ord(state_name) + 1)
                unmarked_states.append(next_set_frozen)
            dfa_transitions[(state_name, 'd')] = states_map[next_set_frozen]

    print("  Estados y transiciones:")
    all_states = sorted(states_map.values())
    for state in all_states:
        matching_set = [k for k, v in states_map.items() if v == state][0]
        is_final = 3 in matching_set
        final_mark = " (Final)" if is_final else ""
        print(f"    Estado {state}{final_mark}: {set(matching_set)}")
        for (s, char), next_s in dfa_transitions.items():
            if s == state:
                print(f"      --{char}--> {next_s}")
    print()

    final_states = {v for k, v in states_map.items() if 3 in k}
    non_final = {v for k, v in states_map.items() if 3 not in k}
    
    print("Minimización por Particiones:")
    particiones = [non_final, final_states] if non_final and final_states else [final_states | non_final]
    print(f"  π₀: {particiones}")
    
    iteracion = 1
    while True:
        nuevas_particiones = []
        cambio = False
        
        for grupo in particiones:
            if len(grupo) <= 1:
                nuevas_particiones.append(grupo)
                continue
            
            subgrupos = {}
            for estado in grupo:
                destino = dfa_transitions.get((estado, 'd'))
                if destino:
                    for idx, part in enumerate(particiones):
                        if destino in part:
                            clave = idx
                            break
                else:
                    clave = -1
                
                if clave not in subgrupos:
                    subgrupos[clave] = set()
                subgrupos[clave].add(estado)
            
            if len(subgrupos) > 1:
                cambio = True
                nuevas_particiones.extend(subgrupos.values())
                print(f"  π₁: {nuevas_particiones} (refinamiento)")
            else:
                nuevas_particiones.append(grupo)
        
        if not cambio:
            print(f"  No hay refinamiento. DFA mínimo alcanzado\n")
            break
        
        particiones = nuevas_particiones
        iteracion += 1

    # SIMULACIÓN DEL AUTÓMATA - Se ejecuta en el método nextToken() del Scanner
    def simulate(word):
        print(f"Demostración de Funcionamiento - Lexema: '{word}'")
        curr = 'A'
        for char in word:
            if '0' <= char <= '9': 
                next_s = dfa_transitions.get((curr, 'd'))
                print(f"  '{char}': Estado {curr} --d--> Estado {next_s}")
                curr = next_s
            else:
                print(f"  '{char}': Símbolo no reconocido (no está en [0-9])")
                return False
        
        final_check = curr in final_states
        print(f"  Resultado: {'ACEPTADO ✓' if final_check else 'RECHAZADO ✗'}\n")
        return final_check

    lexema_input = input("Ingrese un lexema numérico a evaluar: ")
    simulate(lexema_input)

if __name__ == "__main__":
    build_logic_and_simulate()