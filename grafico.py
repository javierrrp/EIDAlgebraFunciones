import math
import matplotlib.pyplot as plt
from sympy import symbols
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

# configuración de sympy
x=symbols("x")
transformacion=tuple(standard_transformations)+(
    implicit_multiplication_application,
    convert_xor
)

# funciones auxiliares
def analizar_funcion(texto_funcion: str):
    return parse_expr(texto_funcion, transformations=transformacion, evaluate=True)

def evaluar_punto(expresion, valor_x: float):
    try:
        resultado=expresion.subs(x, valor_x)
        if resultado.is_real and not resultado.is_infinite:
            return float(resultado.evalf())
    except Exception:
        pass
    return None

# gráfico principal
def grafico_funcion(texto_funcion: str, valor_x: float=None,
                    ventana=(-10,10), paso=0.05, titulo=None):
    expresion=analizar_funcion(texto_funcion)
    xs, ys=[], []

    a, b=ventana
    t=a
    while t <= b:
        y=evaluar_punto(expresion, t)
        if y is not None and math.isfinite(y):
            xs.append(t)
            ys.append(y)
        else:
            if xs:
                plt.plot(xs, ys, "b")
                xs, ys=[], []
        t+=paso
    if xs:
        plt.plot(xs, ys, "b", label="f(x)")

    if valor_x is not None:
        y_eval=evaluar_punto(expresion, valor_x)
        if y_eval is not None:
            plt.scatter([valor_x], [y_eval], color="red",
                        label=f"f({valor_x})={y_eval:.1f}")
            
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(titulo or f"f(x)={texto_funcion}")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    grafico_funcion("(x^3-4x)/(x-2)", valor_x=3, ventana=(-6,6), paso=0.01)
