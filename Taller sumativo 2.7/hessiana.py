import sympy as sp
import numpy as np


def derivada_parcial(funcion, var):
    return sp.diff(funcion, var)


def obtener_variables(expresion):
    expresion_sym = sp.sympify(expresion)
    variables = []

    for simbolo in sp.preorder_traversal(expresion_sym):
        if simbolo.is_Symbol and simbolo.name not in variables:
            variables.append(simbolo.name)
    return variables


def obtener_gradiente(funcion):
    variables = obtener_variables(funcion)
    variables.sort()
    gradiente = []
    expresion_sym = sp.sympify(funcion)

    for var in variables:
        gradiente.append(derivada_parcial(expresion_sym, var))
    return gradiente, variables


def obtener_hessiana(gradiente, variables):
    hessiana = sp.zeros(len(variables), len(variables))

    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            derivada2 = derivada_parcial(gradiente[i], var2)
            hessiana[i, j] = derivada2
    return hessiana


f = input("Ingrese la función: ")
variables = obtener_variables(f)

gradiente, variables = obtener_gradiente(f)
hessiana = obtener_hessiana(gradiente, variables)

print("Gradiente: \n", gradiente)
print("Hessiana: ")
print(hessiana)
