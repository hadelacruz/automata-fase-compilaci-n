#Autor: Humberto Alexander de la Cruz - 23735

from lexemas import mostrar_lexemas
from arbol_sintactico import construir_arbol, calcular_funciones, calcular_followpos
from dfa import construir_dfa
from minimizacion import minimizar_dfa
from simulador import simular_automata

def main():
    # Módulo 1: Mostrar lexemas
    regex = mostrar_lexemas()
    
    # Módulo 2: Construir árbol sintáctico
    root, n1, n2, n2_star, cat1, n3 = construir_arbol(regex)
    
    # Módulo 3: Calcular funciones
    calcular_funciones(root)
    
    # Módulo 4: Calcular followpos
    followpos = calcular_followpos(n1, n2, cat1)
    
    # Módulo 5: Construir DFA
    states_map, dfa_transitions = construir_dfa(root, followpos)
    
    # Módulo 6: Minimizar DFA
    final_states = minimizar_dfa(states_map, dfa_transitions)
    
    # Módulo 7: Simular autómata
    simular_automata(dfa_transitions, final_states)

if __name__ == "__main__":
    main()
