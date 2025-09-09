import sympy as sp


x = sp.symbols('x')

def evaluar_funcion(expresion, valor = None):

    # Definir la funcion
    funcion = sp.sympify(expresion)


    dominio = sp.calculus.util.continuous_domain(funcion, x, sp.Reals)

    recorrido = sp.calculus.util.function_range(funcion, x, dominio)

    resultado = funcion.subs(x, valor).evalf()

    return funcion, resultado, dominio, recorrido

def get_recorrido(funcion, recorrido):
    return (f"El recorrido de la funcion {funcion} es: {recorrido}")

def get_dominio(funcion, dominio):
    return (f"El dominio de la funcion {funcion} es: {dominio}")

funcion, resultado, dominio, recorrido = evaluar_funcion("1/(x-2)", 2)

print("Resultado:", resultado)
print(get_dominio(funcion, dominio))
print(get_recorrido(funcion, recorrido))