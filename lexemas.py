#Autor: Humberto Alexander de la Cruz - 23735

def mostrar_lexemas():
    regex_keywords = "public|class|if|else|static|void"
    regex_numerics = "d d*"
    
    print("=== ANALIZADOR LÉXICO ===\n")
    print("Lexemas identificados:")
    print(f"  1. Keywords: {regex_keywords}")
    print(f"  2. Literales Numéricos: {regex_numerics} (d = [0-9])")
    print(f"\nLexema seleccionado: Literales Numéricos ({regex_numerics})\n")
    
    return regex_numerics
