from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QFormLayout,
                             QFrame)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

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

        left_panel = QFrame()
        left_panel.setObjectName("panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(25, 25, 25, 25)
        left_layout.setSpacing(15)
        
        title_label = QLabel("Panel de Control")
        title_label.setObjectName("h1")
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Ej: (x**3 - 1) / (x - 1)")
        
        self.x_value_input = QLineEdit()
        self.x_value_input.setPlaceholderText("Ej: 5")
        
        form_layout.addRow(QLabel("Función f(x):"), self.function_input)
        form_layout.addRow(QLabel("Evaluar en x:"), self.x_value_input)

        self.analyze_button = QPushButton("Analizar Función")
        self.analyze_button.setIcon(QIcon.fromTheme("system-search"))
        self.analyze_button.setIconSize(QSize(24, 24))

        results_title = QLabel("Resultados")
        results_title.setObjectName("h2")
        
        self.domain_label = QLabel("Dominio: ...")
        self.intercepts_label = QLabel("Intersecciones: ...")
        self.evaluation_label = QLabel("Evaluación: ...")
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")


        #Botones
        self.x2_button = QPushButton("x\u00B2")
        self.x2_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.x3_button = QPushButton("x\u00B3")
        self.x3_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.exp_button = QPushButton("^")
        self.exp_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.parentesisopen_button = QPushButton("(")
        self.parentesisopen_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        self.parentesisclose_button = QPushButton(")")
        self.parentesisclose_button.setFixedSize(40, 40)  # Ajusta según el tamaño necesario

        left_layout.addWidget(title_label)
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.analyze_button)
        left_layout.addSpacing(20)
        left_layout.addWidget(results_title)
        left_layout.addWidget(self.domain_label)
        left_layout.addWidget(self.intercepts_label)
        left_layout.addWidget(self.evaluation_label)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10) # Espacio entre los botones

        # 2. Añadir los botones al layout horizontal
        buttons_layout.addWidget(self.x2_button)
        buttons_layout.addWidget(self.x3_button)
        buttons_layout.addWidget(self.exp_button)
        buttons_layout.addWidget(self.parentesisopen_button)
        buttons_layout.addWidget(self.parentesisclose_button)
        buttons_layout.addStretch() # Empuja los botones a la izquierda

        # 3. Añadir el layout de botones al layout vertical principal
        left_layout.addLayout(buttons_layout)

        left_layout.addStretch()
        left_layout.addWidget(self.error_label)

        right_panel = QFrame()
        right_panel.setObjectName("panel")
        right_layout = QVBoxLayout(right_panel)
        
        graph_placeholder = QLabel("aca los graficos")
        graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_placeholder.setObjectName("graphPlaceholder")
        right_layout.addWidget(graph_placeholder)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
    def apply_styles(self):
        BG_COLOR = "#2c3e50"
        PRIMARY_COLOR = "#34495e"
        SECONDARY_COLOR = "#1abc9c"
        TEXT_COLOR = "#ecf0f1"
        ERROR_COLOR = "#e74c3c"

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
                background-color: {PRIMARY_COLOR};
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
                background-color: {SECONDARY_COLOR};
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: #16a085;
            }}
            QLabel#graphPlaceholder {{
                font-size: 20px;
                color: #bdc3c7;
                border: 2px dashed {PRIMARY_COLOR};
                border-radius: 12px;
                background-color: {BG_COLOR};
            }}
            QLabel#errorLabel {{
                color: {ERROR_COLOR};
                font-weight: bold;
            }}
        """
        self.setStyleSheet(style_sheet)