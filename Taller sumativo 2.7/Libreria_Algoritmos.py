from sympy import *
import numpy as np


def obtener_variables(expresion):
    expresion_sym = sympify(expresion)
    variables = []

    for simbolo in preorder_traversal(expresion_sym):
        if simbolo.is_Symbol and simbolo.name not in variables:
            variables.append(simbolo.name)
    return variables


def Calculo_fx(var, x, funcion):  # función que nos calcula el x evaluado en f(x)
    return funcion.subs(var, x)  # funcion.arg('funcion')


def calculo_derivada_aproximada(x, delta_x, var, funcion):
    dx = (Calculo_fx(var, x + delta_x, funcion) -
          Calculo_fx(var, x, funcion)) / delta_x
    return dx


def derivada_Parcial(funcion, var):
    return diff(funcion, var)


def obtener_gradiente(funcion_string, x, delta_x):

    funcion = sympify(funcion_string)
    variables = obtener_variables(funcion)
    variables.sort()

    gradiente = []
    gradiente_aproximado = []

    i = 0
    for var in variables:

        derivada_parcial = derivada_Parcial(funcion, var)

        gradiente.append(derivada_parcial)
        gradiente_aproximado.append(
            calculo_derivada_aproximada(x[i], delta_x[i], var, funcion))
        i += 1
    return gradiente


def hessian(funcion_string):
    funcion = sympify(funcion_string)
    variables = obtener_variables(funcion)
    variables.sort()
    
    gradiente = [diff(funcion_string, var) for var in variables]
    largo = len(gradiente)

    hessian = np.zeros((largo, largo))

    for i in range(largo):
        for j in range(largo):
            hessian[i][j] = diff(gradiente[i], variables[j])

    return gradiente

