#Autor: Humberto Alexander de la Cruz - 23735

def minimizar_dfa(states_map, dfa_transitions):
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
    
    return final_states
