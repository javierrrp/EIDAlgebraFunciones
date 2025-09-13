from ast import expr
import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy.solvers import solveset
from sympy import S, Union, FiniteSet, Interval, oo
from Model import grafico


def conversion_numeros(val):
        try:
            val_eval = sp.N(val)
            if val_eval == int(val_eval):
                return str(int(val_eval))
            else:
                return f"{float(val_eval):.4f}".rstrip('0').rstrip('.')
        except Exception:
            return str(val)


class Controller:
    def __init__(self, view):
        self.view = view
        self.model = grafico
        self._connect_signals()
        

    def _connect_signals(self):
        self.view.analyze_button.clicked.connect(self.run_analysis)


        buttons = {
            self.view.x2_button: '**2',
            self.view.x3_button: '**3',
            self.view.exp_button: '**',
            self.view.parentesisopen_button: '(',
            self.view.parentesisclose_button: ')',
            self.view.plus_button: '+',
            self.view.minus_button: '-',
            self.view.multiply_button: '*',
            self.view.divide_button: '/',
            self.view.raiz_button: 'sqrt()',
            self.view.x_button: 'x',
            self.view.pi_button: 'pi',
            self.view.e_button: 'e',
            self.view.point_button: '.',
            self.view.sin_button: 'sin()',
            self.view.cos_button: 'cos()',
            self.view.tan_button: 'tan()',
            self.view.log_button: 'log()',
            self.view.ln_button: 'ln()'
        }

        for btn, text in buttons.items():
            btn.clicked.connect(lambda _, t=text: self._insert_text_at_cursor(t))
        
        self.view.clear_button.clicked.connect(self.view.function_input.clear)
        self.view.del_button.clicked.connect(self.view.function_input.backspace)
        self.view.steptostep_button.clicked.connect(self.show_step_by_step)


    def _insert_text_at_cursor(self, text):
        self.view.function_input.insert(text)
        if '()' in text:
            self.view.function_input.cursorBackward(False, 1)
        self.view.function_input.setFocus()


    def _format_domain(self, domain):
            """Convierte el objeto de dominio de sympy en un string legible."""

            def format_endpoint(p):
                if p == oo: return "∞"
                if p == -oo: return "-∞"
                return f"{float(p.evalf()):.3g}"

            if domain == S.Reals:
                return "Todos los reales (ℝ)"

            if isinstance(domain, sp.Complement) and isinstance(domain.args[1], FiniteSet):
                points = sorted([p.evalf() for p in domain.args[1]], key=float)
                points_str = ", ".join([format_endpoint(p) for p in points])
                return f"Todos los reales excepto x = {points_str}"

            if isinstance(domain, Union):
                parts = []
                for interval in domain.args:
                    if isinstance(interval, Interval):
                        start = format_endpoint(interval.start)
                        end = format_endpoint(interval.end)
                        left_bracket = "[" if not interval.left_open else "("
                        right_bracket = "]" if not interval.right_open else ")"
                        parts.append(f"{left_bracket}{start}, {end}{right_bracket}")
                return " U ".join(parts)
            return str(domain)

    def generar_pasos(self, expr, valor_x):
        pasos = []
        x = sp.symbols('x')

        # Paso 1: Mostrar la función ingresada
        pasos.append(f"Función ingresada: f(x) = {expr}")

        # Paso 2: Sustituir x en la expresión como string (sin simplificar aún)
        expr_str = str(expr)
        expr_sust_str = expr_str.replace("x", f"({conversion_numeros(valor_x)})")
        pasos.append(f"Sustituimos x = {conversion_numeros(valor_x)}: {expr_sust_str}")

        # Paso 3: Calcular paso a paso usando sympy para simplificar
        expr_calc = sp.sympify(expr_sust_str)
        if expr_calc != sp.sympify(expr_str):
            pasos.append(f"Calculamos: {conversion_numeros(expr_calc)}")

        # Paso 4: Resultado final
        resultado = expr.subs(x, valor_x).evalf()
        pasos.append(f"Resultado final: f({conversion_numeros(valor_x)}) = {conversion_numeros(resultado)}")

        return pasos


    def show_step_by_step(self):
        function_text = self.view.function_input.text()
        x_text = self.view.x_value_input.text()
        if not function_text or not x_text:
            self.view.error_label.setText("⚠️ Ingresa la función y un valor de x.")
            return

        try:
            expr = self.model.analizar_funcion(function_text)
            valor_x = float(sp.sympify(x_text).evalf())
        except Exception:
            self.view.error_label.setText("⚠️ Valor de x inválido.")
            return

        pasos = self.generar_pasos(expr, valor_x)
        
        from View.paso_a_paso import PasoAPasoDialog
        dialog = PasoAPasoDialog(pasos, parent=self.view)
        dialog.exec()
    
    
    def run_analysis(self):
        self.view.error_label.setText("")
        function_text = self.view.function_input.text()
        x_value_text = self.view.x_value_input.text()

        if not function_text:
            self.view.error_label.setText("⚠️ Error: La función no puede estar vacía.")
            return

        try:
            expr = self.model.analizar_funcion(function_text)
            x = sp.symbols('x')

            domain = continuous_domain(expr, x, sp.S.Reals)
            domain_str = self._format_domain(domain)
            self.view.domain_label.setText(f"<b>Dominio:</b> {domain_str}")

            y_intercept_val = self.model.evaluar_punto(expr, 0)
            y_intercept_str = f"(0, {y_intercept_val:.4g})" if y_intercept_val is not None else "No existe"
            
            x_intercepts = solveset(expr, x, domain=sp.S.Reals)
            if x_intercepts.is_empty:
                x_intercept_str = "No existe"
            else:
                intercept_points = [f"({float(val.evalf()):.4g}, 0)" for val in x_intercepts]
                x_intercept_str = ", ".join(intercept_points)

            self.view.intercepts_label.setText(f"<b>Intersección Eje Y:</b> {y_intercept_str}<br><b>Intersección Eje X:</b> {x_intercept_str}")

            numer, denom = expr.as_numer_denom()
            range_str = "Todos los reales ℝ"

            try:
                if x in numer.free_symbols or x in denom.free_symbols:
                    deg_numer = sp.degree(numer, gen=x)
                    deg_denom = sp.degree(denom, gen=x)

                    if deg_numer == deg_denom:
                        lead_numer = numer.coeff(x**deg_numer)
                        lead_denom = denom.coeff(x**deg_denom)
                        asymptote = lead_numer / lead_denom
                        if asymptote != 0:
                            range_str = f"Todos los reales excepto y = {asymptote}"
                    elif deg_numer < deg_denom:
                        range_str = "Todos los reales excepto y = 0"
            except Exception:
                range_str = "No se pudo determinar automáticamente."

            self.view.range_label.setText(f"<b>Recorrido:</b> {range_str}")

            x_eval = None
            if x_value_text:
                try:
                    x_eval_expr = sp.sympify(x_value_text)
                    x_eval_float = float(x_eval_expr.evalf())

                    y_eval = self.model.evaluar_punto(expr, x_eval_float)

                    if y_eval is not None:
                        self.view.evaluation_label.setText(f"<b>ƒ({x_value_text})</b> = {y_eval:.4g} &nbsp; → &nbsp; <b>Punto:</b> ({x_eval_float:.4g}, {y_eval:.4g})")
                    else:
                        self.view.evaluation_label.setText(f"<b>ƒ({x_value_text})</b> no está definido en el dominio.")

                    x_eval = x_eval_float 

                except (ValueError, sp.SympifyError):
                    self.view.evaluation_label.setText("Valor de x inválido.")
                    x_eval = None
            else:
                self.view.evaluation_label.setText("<b>Evaluación:</b> Ingrese un valor para x.")
            
            ok, mensaje = self.model.grafico_funcion(function_text, valor_x=x_eval, ax=self.view.ax)
            if not ok:
                self.view.error_label.setText(f"⚠️ Error al graficar: {mensaje}")
            
            self.view.canvas.draw()

        except Exception as e:
            self.view.error_label.setText(f"⚠️ Error de sintaxis: {e}")
            self.view.ax.clear()
            self.view.ax.grid(True, alpha=0.3)
            self.view.canvas.draw()
