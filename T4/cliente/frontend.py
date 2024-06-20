from backend import ClientBackend
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout, 
                             QHBoxLayout, QScrollArea, QFormLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
import sys

class ClientFrontend(QMainWindow):
    def __init__(self, config_path):
        super().__init__()
        self.backend = ClientBackend(config_path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Juego de Pepa')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.start_screen()

    def start_screen(self):
        self.clear_layout()

        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/sprites/logo.png")
        scaled_pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio)  # Adjust size
        self.logo.setPixmap(scaled_pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo, 0, 0, 1, 3)

        # Salón de la fama
        self.fame_label = QLabel("Salón de la Fama", self)
        self.fame_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.fame_label.setStyleSheet("font-size: 18px; margin: 10px;")
        self.layout.addWidget(self.fame_label, 1, 0, 1, 1)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.fame_widget = QWidget()
        self.fame_layout = QVBoxLayout()
        self.fame_widget.setLayout(self.fame_layout)

        # Cargar los puntajes (aquí se agregan manualmente para el ejemplo)
        scores = ["Jugador1: 1000", "Jugador2: 900", "Jugador3: 850"]
        for score in scores:
            label = QLabel(score, self)
            self.fame_layout.addWidget(label)

        self.scroll_area.setWidget(self.fame_widget)
        self.scroll_area.setStyleSheet("background-color: #f0f0f0; margin: 10px;")
        self.layout.addWidget(self.scroll_area, 2, 0, 3, 1)

        # Formulario para ingresar nombre de usuario y seleccionar puzzle
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        form_layout.addRow("Nombre de usuario:", self.username_input)

        self.puzzle_dropdown = QComboBox(self)
        self.puzzle_dropdown.addItems(["Puzzle 1", "Puzzle 2", "Puzzle 3"])  # Agrega los nombres de los puzzles disponibles
        form_layout.addRow("Seleccione un puzzle:", self.puzzle_dropdown)

        self.layout.addLayout(form_layout, 2, 1, 1, 2)

        # Botones
        self.start_button = QPushButton("Comenzar partida", self)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.layout.addWidget(self.start_button, 4, 1, 1, 1)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.layout.addWidget(self.exit_button, 4, 2, 1, 1)

    def start_game(self):
        self.username = self.username_input.text()
        self.puzzle = self.puzzle_dropdown.currentText()

        # Conectar al servidor
        self.backend.connect(8000)

        self.game_screen()

    def game_screen(self):
        self.clear_layout()

        self.timer_label = QLabel("Tiempo: 60", self)
        self.layout.addWidget(self.timer_label, 0, 0, 1, 3)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid, 1, 0, 1, 3)

        self.create_game_board()

        self.button_layout = QHBoxLayout()

        self.pause_button = QPushButton("Pausar", self)
        self.pause_button.clicked.connect(self.pause_game)
        self.button_layout.addWidget(self.pause_button)

        self.validate_button = QPushButton("Validar Respuesta", self)
        self.validate_button.clicked.connect(self.validate_solution)
        self.button_layout.addWidget(self.validate_button)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.exit_button)

        self.layout.addLayout(self.button_layout, 2, 0, 1, 3)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = 60
        self.timer.start(1000)

    def create_game_board(self):
        self.board_size = 5  # Example size, should be dynamic based on puzzle
        self.cells = []

        for row in range(self.board_size):
            row_cells = []
            for col in range(self.board_size):
                cell = QLabel(self)
                cell.setFixedSize(40, 40)
                cell.setStyleSheet("border: 1px solid black;")
                cell.setPixmap(QPixmap("assets/sprites/lechuga.png"))
                cell.setScaledContents(True)
                self.grid.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def pause_game(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Reanudar")
        else:
            self.timer.start(1000)
            self.pause_button.setText("Pausar")

    def validate_solution(self):
        solution = "mock_solution"  # Aquí iría la solución real del puzzle
        response = self.backend.send_message(solution)
        if response == "OK":
            self.show_message("Solución correcta")
        else:
            self.show_message("Solución incorrecta")

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(f"Tiempo: {self.time_remaining}")
        if self.time_remaining <= 0:
            self.show_message("Tiempo agotado")
            self.start_screen()

    def show_message(self, message):
        self.clear_layout()
        self.layout.addWidget(QLabel(message, self))
        self.layout.addWidget(QPushButton("Volver a Inicio", self, clicked=self.start_screen))

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            print("Mover hacia arriba")
        elif event.key() == Qt.Key.Key_A:
            print("Mover hacia la izquierda")
        elif event.key() == Qt.Key.Key_S:
            print("Mover hacia abajo")
        elif event.key() == Qt.Key.Key_D:
            print("Mover hacia la derecha")
        elif event.key() == Qt.Key.Key_G:
            print("Marcar/Desmarcar casilla")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frontend = ClientFrontend("config.json")
    frontend.show()
    sys.exit(app.exec())
