import math
import re
import matplotlib.pyplot as plt
from sympy import symbols, sin, cos, tan, log, sqrt, pi, E, solveset, S, sympify, limit, oo
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
        try:
            expr = parse_expr(
                texto,
                transformations=TRANSFORMACIONES,
                local_dict=locales,
                evaluate=False,  # Cambiado a False para mejor control
            )
        except Exception:
            # Fallback con sympify
            expr = sympify(texto, locals=locales, evaluate=False)
        return expr
    except Exception as e:
        # El Controller captura SympifyError como "Error de sintaxis"
        raise SympifyError(str(e))

# ------------------ helpers evaluación ------------------
def _to_real_float(val):
    try:
        if hasattr(val, "is_real") and val.is_real is False:
            return None
        # Manejar infinitos simbólicos
        if val == oo or val == -oo:
            return None
        try:
            vf = complex(val.evalf())
            # Si tiene parte imaginaria significativa, descartar
            if abs(vf.imag) > 1e-10:
                return None
            vf = vf.real
        except Exception:
            vf = float(val)
        if not math.isfinite(vf):
            return None
        return vf
    except Exception:
        return None

# ----------------- evalua expresion con pasos de sustitucion ----------------
def evaluar_punto_con_pasos(expresion, valor_x: float):
    """
    Evalúa una expresión en un punto y muestra el paso a paso de la sustitución
    Retorna: (resultado_float, pasos_texto)
    """
    pasos = []
    
    try:
        # Paso 1: Función original
        funcion_str = str(expresion)
        pasos.append(f"f(x) = {funcion_str}")
        
        # Paso 2: Sustitución
        # Manejar la representación del valor según si es entero o decimal
        if valor_x == int(valor_x):
            # Si es un número entero (como 3.0), mostrarlo sin decimales
            valor_str = str(int(valor_x))
        else:
            # Si es decimal (como 2.5), mostrarlo con decimales
            valor_str = f"{valor_x: .3f}".rstrip('0').rstrip('.')
        
        valor_reemplazo = f'({valor_str})'
        funcion_con_sustitucion = re.sub(r'\bx\b', valor_reemplazo, funcion_str)
        pasos.append(f"f({valor_x}) = {funcion_con_sustitucion}")
    
    
        
        # Paso 3: Mostrar sustitución con SymPy
        expr_sustituida = expresion.subs(x, valor_x)
        if expr_sustituida == int(expr_sustituida):
            # Si es un número entero (e.g., 5.0), lo convertimos a int (5)
            sustitucion_str = str(int(expr_sustituida))
        else:
            # Si no es un entero, lo formateamos para mostrar decimales
            sustitucion_str = f"{expr_sustituida:.3f}"
        pasos.append(f"Sustituyendo x = {valor_x}: {sustitucion_str}")
        
        # Paso 4: Resultado final
        resultado = expresion.subs(x, valor_x).evalf()
        

        try:
            if hasattr(resultado, 'is_real') and resultado.is_real == False:
                resultado_float = None
            elif hasattr(resultado, 'is_finite') and resultado.is_finite == False:
                resultado_float = None
            else:
                resultado_float = float(resultado)
        except (ValueError, TypeError, AttributeError):
            resultado_float = None

            
        if resultado_float is not None:
            pasos.append(f"f({valor_x}) = {resultado_float:.6g}")
        else:
            pasos.append("Resultado: No definido en los reales")
        
        return resultado_float, "\n".join(pasos)
        
    except Exception as e:
        pasos.append(f"Error: {str(e)}")
        return None, "\n".join(pasos)

# ----------------- evalua expresion, devuelve float o none si no es valido en R ----------------
def evaluar_punto(expresion, valor_x: float):
    try:
        # Para funciones racionales, intentar simplificar primero
        expr_trabajo = expresion
        try:
            expr_trabajo = expresion.simplify()
        except Exception:
            pass
        
        # Sustituir el valor
        y = expr_trabajo.subs(x, valor_x)
        
        # Si el resultado aún contiene x, puede ser una indeterminación
        if y.has(x):
            try:
                y = limit(expresion, x, valor_x)
            except Exception:
                return None
        
        # Manejar casos especiales de SymPy
        if hasattr(y, 'is_finite') and y.is_finite is False:
            return None
        if hasattr(y, 'is_real') and y.is_real is None:
            return None
        
        return _to_real_float(y)
    except (ZeroDivisionError, ValueError):
        return None
    except Exception as e:
        # Manejar específicamente el error de formato que mencionaste
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in ["format", "zero._format", "sympify", "nan"]):
            return None
        return None
    
    

def obtener_asintotas_verticales(expr, ventana=(-10, 10)):
    """Detecta asíntotas verticales"""
    asintotas = []
    try:
        expr_simplificada = expr.simplify()
        num, den = expr_simplificada.as_numer_denom()
        
        try:
            soluciones = solveset(den, x, domain=S.Reals)
            for sol in soluciones:
                try:
                    val = float(sol.evalf())
                    if ventana[0] < val < ventana[1]:
                        # Verificar que sea asíntota real, no discontinuidad removible
                        num_val = num.subs(x, sol)
                        if abs(num_val) > 1e-10:
                            asintotas.append(val)
                except Exception:
                    continue
        except Exception:
            pass
    except Exception:
        pass
    
    return sorted(list(set(asintotas)))

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

    # Detectar y marcar asíntotas verticales
    try:
        asintotas = obtener_asintotas_verticales(expr, ventana=(a, b))
        for v in asintotas:
            ax.axvline(v, color='red', linestyle='--', linewidth=1, alpha=0.7)
    except Exception:
        pass

    # Muestreo y trazado
    try:
        xs = _linspace(a, b, paso)
        seg_x, seg_y = [], []
        prev_y = None

        def _flush_segment():
            if len(seg_x) > 1:  # Solo dibujar segmentos con al menos 2 puntos
                try:
                    ax.plot(seg_x, seg_y, "b", linewidth=1.5)
                except Exception:
                    pass
            seg_x.clear()
            seg_y.clear()

        for t in xs:
            y = evaluar_punto(expr, t)
            if y is not None:
                # Detectar saltos grandes para manejar discontinuidades
                if prev_y is not None and abs(y - prev_y) > 1000:
                    _flush_segment()
                
                seg_x.append(t)
                seg_y.append(y)
                prev_y = y
            else:
                _flush_segment()
                prev_y = None

        _flush_segment()

        # Marca de punto evaluado
        if valor_x is not None:
            y_eval = evaluar_punto(expr, valor_x)
            if y_eval is not None:
                try:
                    ax.scatter([valor_x], [y_eval], color="red", s=50, zorder=5,
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