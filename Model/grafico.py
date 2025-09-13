import math
import re
import matplotlib.pyplot as plt
from sympy import symbols, sin, cos, tan, log, sqrt, pi, E
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

# ------------------- configuración SymPy -------------------
x = symbols("x")
TRANSFORMACIONES = tuple(standard_transformations) + (
    implicit_multiplication_application,  # 2x -> 2*x
    convert_xor,                          # ^ -> **
)

# ------------------ normalización de texto del usuario ------------------
def _normalizar_texto(s: str) -> str:
    s = s.strip()
    s = (
        s.replace("×", "*")
         .replace("÷", "/")
         .replace("π", "pi")
         .replace("√", "sqrt")
         .replace(",", ".")  # coma decimal -> punto
    )
    # corrige sqrt9 -> sqrt(9), sqrtx -> sqrt(x)
    s = re.sub(r"sqrt\s*([A-Za-z0-9\(])", r"sqrt(\1", s)
    # balanceo mínimo de paréntesis (cierra los que falten)
    if s.count("(") > s.count(")"):
        s += ")" * (s.count("(") - s.count(")"))
    return s

# ------------------ convertidor en objeto matematico ------------------
def analizar_funcion(texto_funcion: str):
    locales = {
        "x": x,
        # trigonométricas
        "sin": sin, "cos": cos, "tan": tan,
        # log/raíz
        "log": log, "ln": log, "sqrt": sqrt,
        # constantes
        "pi": pi, "e": E, "E": E,
    }
    try:
        texto = _normalizar_texto(texto_funcion)
        expr = parse_expr(
            texto,
            transformations=TRANSFORMACIONES,
            local_dict=locales,
            evaluate=True,
        )
        return expr
    except Exception as e:
        # El Controller captura SympifyError como “Error de sintaxis”
        raise SympifyError(str(e))

# ------------------ helpers evaluación ------------------
def _to_real_float(val):
    try:
        if hasattr(val, "is_real") and val.is_real is False:
            return None
        vf = float(val.evalf())
        if not math.isfinite(vf):
            return None
        return vf
    except Exception:
        return None
# ----------------- evalua expresion, devuelve float o none si no es valido en R ----------------
def evaluar_punto(expresion, valor_x: float):
    try:
        y = expresion.subs(x, valor_x)
        return _to_real_float(y)
    except Exception:
        return None

# ------------------ muestreo lineal ------------------
def _linspace(a: float, b: float, paso: float, max_puntos: int = 20000):
    if paso <= 0:
        raise ValueError("El paso debe ser positivo.")
    if a >= b:
        raise ValueError("Ventana inválida: se requiere a < b.")
    puntos = int((b - a) / paso) + 1
    if puntos > max_puntos:
        paso = (b - a) / max_puntos
        puntos = max_puntos
    xs = []
    t = a
    # epsilon para cubrir el borde derecho con acumulación flotante
    for _ in range(puntos):
        xs.append(t)
        t += paso
    if xs and xs[-1] < b:
        xs.append(b)
    return xs

# ------------------ gráfico principal (contrato ok/detail) ------------------
def grafico_funcion(
    texto_o_expr,
    valor_x: float = None,
    ventana=(-10, 10),
    paso=0.05,
    titulo=None,
    ax=None,
):
    # Validar ventana y paso
    try:
        a, b = float(ventana[0]), float(ventana[1])
        paso = float(paso)
        if a >= b:
            return (False, "Ventana inválida: se requiere a < b.")
        if paso <= 0:
            return (False, "El paso debe ser positivo.")
    except Exception as e:
        return (False, f"Parámetros de ventana/paso inválidos: {e}")

    # Preparar expresión
    try:
        if hasattr(texto_o_expr, "free_symbols"):
            expr = texto_o_expr
            texto_funcion = str(texto_o_expr)
        else:
            expr = analizar_funcion(texto_o_expr)
            texto_funcion = str(texto_o_expr)
    except SympifyError as e:
        return (False, f"Error al interpretar la función: {e}")
    except Exception as e:
        return (False, f"No se pudo preparar la función: {e}")

    # Preparar ejes
    created_fig = False
    try:
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
    except Exception as e:
        return (False, f"No se pudo preparar los ejes/figura: {e}")

    # Muestreo y trazado
    try:
        xs = _linspace(a, b, paso)
        seg_x, seg_y = [], []

        def _flush_segment():
            if seg_x:
                try:
                    ax.plot(seg_x, seg_y, "b", label="f(x)")
                except Exception:
                    pass
            seg_x.clear()
            seg_y.clear()

        for t in xs:
            y = evaluar_punto(expr, t)
            if y is not None:
                seg_x.append(t)
                seg_y.append(y)
            else:
                _flush_segment()

        _flush_segment()

        # Marca de punto evaluado
        if valor_x is not None:
            y_eval = evaluar_punto(expr, valor_x)
            if y_eval is not None:
                try:
                    ax.scatter([valor_x], [y_eval], color="red",
                               label=f"f({valor_x}) = {y_eval:.4g}")
                except Exception:
                    # no es bloqueante
                    pass

        try:
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend(loc="best")
        except Exception:
            pass

    except Exception as e:
        if created_fig:
            try:
                plt.close(fig)
            except Exception:
                pass
        return (False, f"No se pudo trazar la función: {e}")

    return (True, None)
