#Autor: Humberto Alexander de la Cruz - 23735

def simular_automata(dfa_transitions, final_states):
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
