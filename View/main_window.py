from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QFormLayout,
                             QFrame, QCompleter, QSizePolicy)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from Model.grafico import grafico_funcion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EID Algebra")
        self.setWindowIcon(QIcon.fromTheme("applications-science"))
        self.setGeometry(100, 100, 950, 500)

        self.apply_styles()
        

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Título
        layout.addWidget(self._make_label("⚡ Panel de Control", "h1"))

        # Sección de entrada (Formulario)
        form_layout = QFormLayout()

        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: (x**3 - 1) / (x - 1)")
        self.function_input.setObjectName("functionInput")
        self.function_input.setMinimumHeight(50)
        self.function_input.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        self.function_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        completer = QCompleter(["sin", "cos", "tan", "log", "ln", "sqrt", "pi", "e"])
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.function_input.setCompleter(completer)
        
        form_layout.addRow(self._make_label("ƒ(x) =", "fxLabel"), self.function_input)

        self.x_value_input = QLineEdit()
        self.x_value_input.setPlaceholderText("Ej: 5")
        self.x_value_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        form_layout.addRow("Evaluar en x:", self.x_value_input)
        layout.addLayout(form_layout)
        
        # Botones principales (Analizar y Paso a Paso)
        self.analyze_button = self._make_button("Analizar Función", "system-search")
        self.steptostep_button = self._make_button("Paso a Paso", "document-edit")
        
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.steptostep_button)
        layout.addSpacing(20)
        
        # Sección de resultados
        layout.addWidget(self._make_label("📊 Resultados", "h2"))

        self.domain_label = QLabel("Dominio: ...")
        self.range_label = QLabel("Recorrido: ...")
        self.intercepts_label = QLabel("Intersecciones: ...")
        self.evaluation_label = QLabel("Evaluación: ...")
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")

        for label in [self.domain_label, self.range_label, self.intercepts_label, self.evaluation_label]:
            label.setWordWrap(True)
            layout.addWidget(label)
            
        layout.addStretch()  # Este espaciador empuja los botones de la calculadora hacia abajo
        
        # Botones de operadores y números (calculadora)
        button_grid = [[("x²", "x2_button"), ("x³", "x3_button"), ("^", "exp_button"), ("(", "parentesisopen_button"), (")", "parentesisclose_button")],
                       [("+", "plus_button"), ("-", "minus_button"), ("×", "multiply_button"), ("÷", "divide_button"), ("=", "equal_button")],
                       [("√", "raiz_button"), ("x", "x_button"), ("π", "pi_button"), ("e", "e_button"), (".", "point_button")],
                       [("sin", "sin_button"), ("cos", "cos_button"), ("tan", "tan_button"), ("log", "log_button"), ("ln", "ln_button")],
                       [("1", "button_1"), ("2", "button_2"), ("3", "button_3"), ("4", "button_4"), ("5", "button_5")],
                       [("6", "button_6"), ("7", "button_7"), ("8", "button_8"), ("9", "button_9"), ("0", "button_0")]]

        for row in button_grid:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            for text, attr in row:
                btn = QPushButton(text)
                # Se eliminó el setFixedSize, ahora los botones se adaptan
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                setattr(self, attr, btn)
                row_layout.addWidget(btn)
            layout.addLayout(row_layout)
        
        # Botones de control
        control_layout = QHBoxLayout()
        self.clear_button = QPushButton("C")
        self.del_button = QPushButton("DEL")
        for btn in [self.clear_button, self.del_button]:
            # Se eliminó el setFixedSize, ahora los botones se adaptan
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            control_layout.addWidget(btn)
        layout.addLayout(control_layout)

        layout.addWidget(self.error_label)

        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)

        layout.addWidget(self.canvas)
        return panel

    def _make_button(self, text, icon_name=None):
        btn = QPushButton(text)
        if icon_name:
            btn.setIcon(QIcon.fromTheme(icon_name))
            btn.setIconSize(QSize(24, 24))
        return btn

    def _make_label(self, text, obj_name=None):
        label = QLabel(text)
        if obj_name:
            label.setObjectName(obj_name)
        return label

        
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