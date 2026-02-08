# Analizador Léxico - DFA para Literales Numéricos

**Autor:** Humberto Alexander de la Cruz - 23735

## Descripción

Implementación del algoritmo de construcción directa de un DFA para reconocer literales numéricos.

## Características

- Identificación de lexemas del código Java
- Construcción de árbol sintáctico
- Cálculo de funciones: nullable, firstpos, lastpos, followpos
- Construcción del DFA
- Minimización por particiones
- Simulación del autómata

## Ejecución

```bash
python analizador.py
```

## Video Demostrativo

### https://youtu.be/SlzQQRXsRBQ

## Estructura del Proyecto

```
├── analizador.py          # Archivo principal
├── node.py                # Clase Node
├── lexemas.py             # Identificación de lexemas
├── arbol_sintactico.py    # Construcción del árbol
├── dfa.py                 # Construcción del DFA
├── minimizacion.py        # Minimización
└── simulador.py           # Simulación
```

## Requisitos

- Python 3.x
