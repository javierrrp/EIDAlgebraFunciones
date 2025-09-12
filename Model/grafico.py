import math
import re
import matplotlib.pyplot as plt
from sympy import symbols, sin, cos, tan, log, sqrt, pi, E
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

# -------------------configuración SymPy ------------------
x = symbols("x")
TRANSFORMACIONES = tuple(standard_transformations) + (
    implicit_multiplication_application,  # 2x -> 2*x
    convert_xor                           # ^ -> **
)

# ------------------ normalización de texto del usuario ------------------
def _normalizar_texto(s: str) -> str:
    s = s.strip()
    s = (s.replace("×", "*")
           .replace("÷", "/")
           .replace("π", "pi")
           .replace("√", "sqrt")
           .replace(",", "."))  # coma decimal a punto

    # corrige casos como sqrt9 -> sqrt(9), sqrtx -> sqrt(x)
    s = re.sub(r"sqrt\s*([A-Za-z0-9\(])", r"sqrt(\1", s)
    if s.count("(") > s.count(")"):
        s += ")" * (s.count("(") - s.count(")"))
    return s

# ------------------ funciones auxiliares ------------------
def analizar_funcion(texto_funcion: str):
    locales = {"x": x, "sin": sin, "cos": cos, "tan": tan,
               "log": log, "ln": log, "sqrt": sqrt, "pi": pi, "e": E}
    texto = _normalizar_texto(texto_funcion)
    expr = parse_expr(texto, transformations=TRANSFORMACIONES,
                      local_dict=locales, evaluate=True)
    return expr

# evalúa la expresión en x=valor_x devolviendo float o none si no es válido.
def evaluar_punto(expresion, valor_x: float):
    try:
        y = expresion.subs(x, valor_x)
        if y.is_real and not y.is_infinite:
            y = float(y.evalf())
            if math.isfinite(y):
                return y
    except Exception:
        pass
    return None

# ------------------ gráfico principal ------------------
def grafico_funcion(texto_funcion: str, valor_x: float = None,
                    ventana=(-10, 10), paso=0.05, titulo=None, ax=None):
    expr = analizar_funcion(texto_funcion)

    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        created_fig = True
    else:
        fig = ax.figure

    ax.clear()
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titulo or f"f(x) = {texto_funcion}")

    a, b = ventana
    t = a
    xs, ys = [], []

    while t <= b + 1e-12:
        y = evaluar_punto(expr, t)
        if y is not None:
            xs.append(t); ys.append(y)
        else:
            if xs:
                ax.plot(xs, ys, "b")
                xs, ys = [], []
        t += paso

    if xs:
        ax.plot(xs, ys, "b", label="f(x)")

    if valor_x is not None:
        y_eval = evaluar_punto(expr, valor_x)
        if y_eval is not None:
            ax.scatter([valor_x], [y_eval], color="red",
                       label=f"f({valor_x}) = {y_eval:.4g}")

    ax.legend(loc="best")
    if created_fig:
        return fig, ax
    return ax
