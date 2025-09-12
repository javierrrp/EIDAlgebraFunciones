from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QFormLayout,
                             QFrame, QCompleter)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from Model.grafico import grafico_funcion

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EID Algebra")
        self.setWindowIcon(QIcon.fromTheme("applications-science"))
        self.setGeometry(100, 100, 950, 700)

        self.apply_styles()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

         # -------------------- PANEL IZQUIERDO --------------------
        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(25, 25, 25, 25)
        left_layout.setSpacing(15)

        title_label = QLabel("⚡ Panel de Control")
        title_label.setObjectName("h1")

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Entrada de función con "ƒ(x) ="
        fx_layout = QHBoxLayout()
        fx_label = QLabel("ƒ(x) =")
        fx_label.setObjectName("fxLabel")

        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: (x**3 - 1) / (x - 1)")
        self.function_input.setObjectName("functionInput")
        self.function_input.setMinimumHeight(80)  # Más alto
        self.function_input.setFont(QFont("Consolas", 158, QFont.Weight.Bold))

        # Autocompletado para funciones
        self.functions = ["sin", "cos", "tan", "log", "ln", "sqrt", "pi", "e"]
        completer = QCompleter(self.functions)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.function_input.setCompleter(completer)

        fx_layout.addWidget(fx_label)
        fx_layout.addWidget(self.function_input)

        self.x_value_input = QLineEdit()
        self.x_value_input.setPlaceholderText("Ej: 5")

        form_layout.addRow(fx_layout)
        form_layout.addRow(QLabel("Evaluar en x:"), self.x_value_input)

        self.analyze_button = QPushButton("Analizar Función")
        self.analyze_button.setIcon(QIcon.fromTheme("system-search"))
        self.analyze_button.setIconSize(QSize(24, 24))

        results_title = QLabel("📊 Resultados")
        results_title.setObjectName("h2")

        self.domain_label = QLabel("Dominio: ...")
        self.intercepts_label = QLabel("Intersecciones: ...")
        self.evaluation_label = QLabel("Evaluación: ...")
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")

        #Botones

        # --- Botones de exponentes ---
        self.x2_button = QPushButton("x\u00B2")
        self.x2_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.x3_button = QPushButton("x\u00B3")
        self.x3_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.exp_button = QPushButton("^")
        self.exp_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        # --- Botones de parentesis --- 
        self.parentesisopen_button = QPushButton("(")
        self.parentesisopen_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.parentesisclose_button = QPushButton(")")
        self.parentesisclose_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        # --- Botones de operaciones básicas ---
        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.minus_button = QPushButton("-")
        self.minus_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.multiply_button = QPushButton("×")
        self.multiply_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.divide_button = QPushButton("÷")
        self.divide_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        #--- Boton igual ---
        self.equal_button = QPushButton("=")
        self.equal_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        # --- Raiz ---

        self.raiz_button = QPushButton("√")
        self.raiz_button.setFixedSize(40, 40)

        # --- Variable principal 'x' ---
        self.x_button = QPushButton("x")
        self.x_button.setFixedSize(40, 40)

        # --- Punto decimal ---
        self.point_button = QPushButton(".")
        self.point_button.setFixedSize(40, 40)

        # --- Constantes Matemáticas ---
        self.pi_button = QPushButton("π")
        self.pi_button.setFixedSize(40, 40)
        self.e_button = QPushButton("e")
        self.e_button.setFixedSize(40, 40)

        # --- Funciones Trigonométricas ---
        self.sin_button = QPushButton("sin")
        self.sin_button.setFixedSize(50, 40)
        self.cos_button = QPushButton("cos")
        self.cos_button.setFixedSize(50, 40)
        self.tan_button = QPushButton("tan")
        self.tan_button.setFixedSize(50, 40)

        # --- Funciones Logarítmicas ---
        self.log_button = QPushButton("log")  # Logaritmo base 10
        self.log_button.setFixedSize(50, 40)
        self.ln_button = QPushButton("ln")    # Logaritmo natural
        self.ln_button.setFixedSize(50, 40)

        # --- Botones de control ---
        self.clear_button = QPushButton("C")  # Limpiar todo
        self.clear_button.setFixedSize(40, 40)
        self.del_button = QPushButton("DEL")  # Borrar último caracter
        self.del_button.setFixedSize(40, 40)


        
        #Botones

        left_layout.addWidget(title_label)
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.analyze_button)
        left_layout.addSpacing(20)
        left_layout.addWidget(results_title)
        left_layout.addWidget(self.domain_label)
        left_layout.addWidget(self.intercepts_label)
        left_layout.addWidget(self.evaluation_label)

        

        # --- Crear filas ---
        buttons_fila1_layout = QHBoxLayout()
        buttons_fila1_layout.setSpacing(10)

        buttons_fila2_layout = QHBoxLayout()
        buttons_fila2_layout.setSpacing(10)

        buttons_fila3_layout = QHBoxLayout()
        buttons_fila3_layout.setSpacing(10)

        buttons_fila4_layout = QHBoxLayout()
        buttons_fila4_layout.setSpacing(10)

        # 2. Añadir los botones al layout horizontal
        buttons_fila1_layout.addWidget(self.x2_button)
        buttons_fila1_layout.addWidget(self.x3_button)
        buttons_fila1_layout.addWidget(self.exp_button)
        buttons_fila1_layout.addWidget(self.parentesisopen_button)
        buttons_fila1_layout.addWidget(self.parentesisclose_button)
        buttons_fila1_layout.addStretch() # Empuja los botones a la izquierda

        buttons_fila2_layout.addWidget(self.plus_button)
        buttons_fila2_layout.addWidget(self.minus_button)
        buttons_fila2_layout.addWidget(self.multiply_button)
        buttons_fila2_layout.addWidget(self.divide_button)
        buttons_fila2_layout.addWidget(self.equal_button)


        buttons_fila3_layout.addWidget(self.raiz_button)
        buttons_fila3_layout.addWidget(self.x_button)
        buttons_fila3_layout.addWidget(self.pi_button)
        buttons_fila3_layout.addWidget(self.e_button)
        buttons_fila3_layout.addWidget(self.point_button)
        
        buttons_fila4_layout.addWidget(self.sin_button)
        buttons_fila4_layout.addWidget(self.cos_button)
        buttons_fila4_layout.addWidget(self.tan_button)
        buttons_fila4_layout.addWidget(self.log_button)
        buttons_fila4_layout.addWidget(self.ln_button)


        # 3. Añadir el layout de botones al layout vertical principal
        left_layout.addLayout(buttons_fila1_layout)
        left_layout.addLayout(buttons_fila2_layout)
        left_layout.addLayout(buttons_fila3_layout)
        left_layout.addLayout(buttons_fila4_layout)

        left_layout.addStretch()
        left_layout.addWidget(self.error_label)

        right_panel = QFrame()
        right_panel.setObjectName("panel")
        right_layout = QVBoxLayout(right_panel)
        
        graph_placeholder = QLabel("📈 Gráficos")
        graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_placeholder.setObjectName("graphPlaceholder")
        right_layout.addWidget(graph_placeholder)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
    def apply_styles(self):
        BG_COLOR = "#1e1e2f"
        PANEL_COLOR = "#2a2a40"
        ACCENT_COLOR = "#00d2d3"
        ACCENT_HOVER = "#00a8b5"
        TEXT_COLOR = "#f1f2f6"
        ERROR_COLOR = "#ff6b6b"
        SECONDARY_COLOR = "#1abc9c"

        style_sheet = f"""
            QWidget {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: {TEXT_COLOR};
            }}
            QMainWindow {{
                background-color: {BG_COLOR};
            }}
            QFrame#panel {{
                background-color: {PANEL_COLOR};
                border-radius: 12px;
            }}
            QLabel#h1 {{
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 10px;
            }}
            QLabel#h2 {{
                font-size: 18px;
                font-weight: bold;
                color: {SECONDARY_COLOR};
                padding-top: 10px;
            }}
            QLabel#fxLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {SECONDARY_COLOR};
                margin-right: 6px;
            }}
            QLineEdit#functionInput {{
                background-color: #1e272e;
                border: 2px solid {SECONDARY_COLOR};
                border-radius: 8px;
                padding: 8px;
            }}
            QLineEdit {{
                background-color: {BG_COLOR};
                border: 1px solid {SECONDARY_COLOR};
                border-radius: 6px;
                padding: 8px;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border: 2px solid {SECONDARY_COLOR};
            }}
            QPushButton {{
                background-color: {ACCENT_COLOR};
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
            QLabel#graphPlaceholder {{
                font-size: 20px;
                color: #bdc3c7;
                border: 2px dashed {BG_COLOR};
                border-radius: 12px;
                background-color: {BG_COLOR};
            }}
            QLabel#errorLabel {{
                color: {ERROR_COLOR};
                font-weight: bold;
            }}
        """
        self.setStyleSheet(style_sheet)