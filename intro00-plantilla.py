# -*- mode: python; coding: utf-8; -*-
# PROBLEMAS DE EJERCICIO
# Inteligencia Artificial
# 2023-1
#
# Puede resultarte útil averiguar sobre random.random y random.choice

import random, string

# Ayúdame Python a saber que hace el módulo random :'(
# >>> help(random)
# >>> random?      # funciona solo con ipython
# ¿Qué cosas tiene el módulo random?
# >>> dir(random)

# 1. Escribe un predicado que determina si una cadena de caracteres
# consiste de un caracter que es dígito.
def is_digit(x: str) -> bool:
    return len(x) == 1 and x in "0123456789"
    '''
    if x.isdigit():
        return True
    else:
        return False
    '''
    raise Exception("Not yet implemented")

# 2. Escribe un predicado que determina si una cadena de caracteres
# consiste únicamente de al menos un dígito.
def is_natlike(x: str) -> bool:
    return len(x) > 0 and all(is_digit(c) for c in x)
    '''
    count_digits = 0
    if x is None:
        return False
    for i in range(len(x)):
        if x[i].isdigit():
            count_digits += 1
        else:
            return False
    if count_digits == 1:
        return True
    else:
        return False
    '''
    raise Exception("Not yet implemented")

# 3. Escribe una función que genere una cadena que satisface
# |is_digit| de forma aleatoria.
def rand_digit() -> str:
    return random.choice("0123456789")
    '''
    x = random.randint(0, 9)
    y = str(x)
    if is_natlike(y) == True:
        return y
    print(y)
    '''
    raise Exception("Not yet implemented")

# 4. Escribe una función que dado un entero positivo $n$ genera una
# cadena de caracteres con $n$ dígitos aleatorios.
def rand_natlike(n: int) -> str:
    if n < 1:
        raise ValueError(f'Not a positive integer: {n}')
    return "".join(rand_digit() for _ in range(n))

# 5. Escribe una función que calcule la distancia de Hamming de dos
# cadenas que satisfacen |is_natlike| y que son de la misma longitud.
def natlike_distance(x: str, y: str) -> int:
    if not (is_natlike()):
        if not (is_natlike(x) and is_natlike(y)):
            raise ValueError(f"Both strings must be natlike: {x}, {y}")
        if len(x) != len(y):
            raise ValueError(f"String length mismatch: {len(x)}, {len(y)}")
        return sum(d1 != d2 for d1, d2 in zip(x,y))


# 6. Escribe una función que dada una cadena que satisface
# |is_natlike| regrese la misma cadena pero con un dígito distinto de
# forma aleatoria.
#
# Nota: Debe cambiar exactamente un dígito, es decir:
# natlike_distance(x, natlike_change_one(x)) == 1
def natlike_change_one(x: str) -> str:
    return natlike_change_n(x, 1)
    raise Exception("Not yet implemented")


# 7. Escribe una función que dada una cadena que satisface
# |is_natlike| regrese la misma cadena pero con dos dígitos distintos
# de forma aleatoria.
#
# Nota: Deben cambiar exactamente dos dígitos, es decir:
# natlike_distance(x, natlike_change_two(x)) == 2
def natlike_change_two(x: str) -> str:
    return natlike_change_n(x, 2)
    raise Exception("Not yet implemented")


# 8. Escribe una función que dada una cadena que satisface
# |is_natlike| regrese la misma cadena pero con tres dígitos distintos
# de forma aleatoria.
#
# Nota: Deben cambiar exactamente tres dígitos, es decir:
# natlike_distance(x, natlike_change_three(x)) == 3
def natlike_change_three(x: str) -> str:
    return natlike_change_n(x, 3)
    raise Exception("Not yet implemented")


# 8. Escribe una función que dada una cadena que satisface
# |is_natlike| y un entero no negativo $n$ con magnitud a lo más la
# longitud de la cadena regrese la misma cadena pero con $n$ dígitos
# distinto de forma aleatoria.
#
# Nota: Deben cambiar exactamente $n$ dígitos, es decir:
# natlike_distance(x, natlike_change_n(x, n)) == n
def natlike_change_n(x: str, n: int) -> str:
    if not is_natlike(x):
        raise ValueError(f"String must be natlike: {x}")
    if not (0 <= n <= len(x)):
        raise ValueError(f"String must be at least of length {n}")
    N = len(x)
    m = 0
    y = ""
    for i in range(N):
        if m == n:
            return y + x[i:]
        elif (N - i) * random.random() >= n -m:
            u += x[i]
        else:
            m += 1
            d = random.choice("0123456789".replace(x[i], ""))
            y += d
    return y