from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QFrame, QLabel, QScrollArea
from PyQt6.QtCore import Qt

class PasoAPasoDialog(QDialog):
    def __init__(self, pasos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Análisis Paso a Paso")
        self.setMinimumSize(500, 400)

        # Cambiar a QVBoxLayout en lugar de QFrame
        layout = QVBoxLayout()

        # Título
        title_label = QLabel("📝 Paso a Paso de la Evaluación")
        title_label.setObjectName("titleLabel")

        # Área de pasos
        self.steps_label = QLabel()
        self.steps_label.setObjectName("stepsLabel")
        self.steps_label.setWordWrap(True)
        self.steps_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Mostrar los pasos
        pasos_texto = "\n".join(pasos) if isinstance(pasos, list) else str(pasos)
        self.steps_label.setText(pasos_texto)

        steps_scroll = QScrollArea()
        steps_scroll.setWidget(self.steps_label)
        steps_scroll.setWidgetResizable(True)
        steps_scroll.setObjectName("stepsScroll")

        # Agregar widgets al layout
        layout.addWidget(title_label)
        layout.addWidget(steps_scroll)

        self.setLayout(layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;
                color: #f1f2f6;
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1abc9c;
                padding: 10px;
            }
            QLabel#stepsLabel {
                background-color: #1e272e;
                border: 1px solid #1abc9c;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
                color: #f1f2f6;
            }
            QScrollArea#stepsScroll {
                border: none;
                background-color: transparent;
            }
            QPushButton {
                background-color: #00d2d3;
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #00a8b5;
            }
        """)