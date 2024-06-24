from backend import ClientBackend
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, QGridLayout, 
                             QHBoxLayout, QScrollArea, QFormLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPixmap
import sys
import numpy as np
import json
import os
import pygame
import random

from parametros import *

# Inicializar pygame para el uso de sonidos
pygame.init()

# Constante para el tamaño de las celdas
CELL_SIZE = 23

# Board: clase que representa internamente el estado del juego
class Board:
    def __init__(self, filename):
        self.filename = filename
        self.load_board()
        self.i = 0
        self.j = 0

    def load_board(self):
        with open(self.filename, 'r') as file:
            puzzle_data = file.readlines()
            self.puzzle_up = puzzle_data[0].strip()
            self.puzzle_left = puzzle_data[1].strip()

        self.p_up_list = [list(map(int, x.split(','))) if x != '-' else [0] for x in self.puzzle_up.split(';')]
        self.p_left_list = [list(map(int, x.split(','))) if x != '-' else [0] for x in self.puzzle_left.split(';')]

        self.width = len(self.p_up_list)
        self.height = len(self.p_left_list)
        self.grid = np.ones((self.width, self.height))

    def __str__(self):
        return f"current position: {self.i}, {self.j}\n{self.grid}"
    
    def getCurrentPosition(self):
        return (self.i, self.j)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def moveLeft(self):
        self.j = max(0, self.j-1)

    def moveRight(self):
        self.j = min(self.width-1, self.j+1)

    def moveUp(self):
        self.i = max(self.i-1, 0)

    def moveDown(self):
        self.i = min(self.height-1, self.i+1)

    def eat(self):
        self.grid[self.i][self.j] = 0

    def poop(self):
        self.grid[self.i][self.j] = 2

    def isEmpty(self):
        return self.grid[self.i][self.j] == 0

# GameController: conecta el Board con la pantalla
class GameController:
    def __init__(self, Board, ClientFrontend):
        self.Board = Board
        self.ClientFrontend = ClientFrontend

        self.game_board = self.ClientFrontend.game_board

        self.player = QLabel(self.ClientFrontend)
        self.player.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.player.setStyleSheet("border: 0px solid black;")
        self.player.setPixmap(QPixmap("assets/sprites/pepa/down_0.png"))
        self.player.setScaledContents(True)

        self.updatePlayer(self.player)

    def updatePlayer(self, player):
        i = self.Board.getCurrentPosition()[0]
        j = self.Board.getCurrentPosition()[1]
        player.setParent(None)
        self.game_board.addWidget(player, i, j)

    def updateBoard(self):
        for i in range(self.Board.getHeight()):
            for j in range(self.Board.getWidth()):
                item = self.game_board.itemAtPosition(i, j)
                if item is not None:
                    widget = item.widget()
                    if self.Board.grid[i][j] == 0:
                        widget.setPixmap(QPixmap())
                    elif self.Board.grid[i][j] == 1:
                        widget.setPixmap(QPixmap("assets/sprites/lechuga.png"))
                    elif self.Board.grid[i][j] == 2:
                        widget.setPixmap(QPixmap("assets/sprites/poop.png"))

    def moveLeft(self):
        self.Board.moveLeft()
        self.updatePlayer(self.player)

    def moveRight(self):
        self.Board.moveRight()
        self.updatePlayer(self.player)

    def moveUp(self):
        self.Board.moveUp()
        self.updatePlayer(self.player)

    def moveDown(self):
        self.Board.moveDown()
        self.updatePlayer(self.player)

    def eat_or_poop(self):
        i, j = self.Board.getCurrentPosition()
        if self.Board.isEmpty():
            self.Board.poop()
            self.ClientFrontend.play_sound("poop.wav")
            QTimer.singleShot(TIEMPO_TRANSICION * 1000, lambda: self.convertPoopToLettuce(i, j))
        else:
            self.Board.eat()
            self.ClientFrontend.play_sound("comer.wav")
        self.updateBoard()

    def convertPoopToLettuce(self, i, j):
        self.Board.grid[i][j] = 1
        self.updateBoard()

class Sandia(QLabel):
    def __init__(self, parent, client_frontend):
        super().__init__(parent)
        self.client_frontend = client_frontend
        self.setPixmap(QPixmap("assets/sprites/sandia.png"))
        self.setScaledContents(True)
        self.setFixedSize(40, 40)
        self.setStyleSheet("background: transparent;")
        self.show()

    def mousePressEvent(self, event):
        self.client_frontend.capture_sandia(self)
        super().mousePressEvent(event)

class ClientFrontend(QMainWindow):
    def __init__(self, config_path, port):
        super().__init__()
        self.backend = ClientBackend(config_path)
        self.port = port
        self.muted = False
        self.initUI()
        self.cheat_buffer = []
        self.cheat_codes = {
            'INF': self.activate_infinite_time,
            'MUTE': self.mute_sounds
        }

    def play_sound(self, sound_file):
        if not self.muted:
            pygame.mixer.Sound(f"assets/sonidos/{sound_file}").play()

    def initUI(self):
        self.setWindowTitle('Juego de Pepa')
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.start_screen()
        self.play_sound("musica_1.wav")

    def load_board(self, filename):
        self.board = Board(filename)
        self.connectBoardToGridLayout(self.board, self.row_indicator, self.col_indicator, self.game_board)
        self.controller = GameController(self.board, self)

    def start_screen(self):
        self.stop_timers()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.logo = QLabel(self)
        pixmap = QPixmap("assets/sprites/logo.png")
        scaled_pixmap = pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(scaled_pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo, 0, 0, 1, 3)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.fame_widget = QWidget()
        self.fame_layout = QVBoxLayout()
        self.fame_widget.setLayout(self.fame_layout)

        scores = self.load_scores()
        for name, score in scores:
            label = QLabel(f"{name}: {score}", self)
            self.fame_layout.addWidget(label)

        self.scroll_area.setWidget(self.fame_widget)
        self.scroll_area.setStyleSheet("background-color: #000000; margin: 10px;")
        self.layout.addWidget(self.scroll_area, 2, 0, 3, 1)

        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        form_layout.addRow("Nombre de usuario:", self.username_input)

        self.puzzle_dropdown = QComboBox(self)
        self.puzzle_dropdown.addItems(self.load_puzzles())
        form_layout.addRow("Seleccione un puzzle:", self.puzzle_dropdown)

        self.layout.addLayout(form_layout, 2, 1, 1, 2)

        self.start_button = QPushButton("Comenzar partida", self)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.layout.addWidget(self.start_button, 4, 1, 1, 1)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.layout.addWidget(self.exit_button, 4, 2, 1, 1)

    def load_scores(self):
        scores = []
        if os.path.exists("puntaje.txt"):
            with open("puntaje.txt", "r") as file:
                for line in file:
                    name, score = line.strip().split(': ')
                    scores.append((name, float(score)))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def load_puzzles(self):
        puzzles = []
        base_puzzles_path = "assets/base_puzzles"
        for filename in os.listdir(base_puzzles_path):
            if filename.endswith(".txt"):
                puzzles.append(filename)
        return puzzles

    def start_game(self):
        self.username = self.username_input.text()
        if not self.validate_username(self.username):
            return

        self.puzzle = self.puzzle_dropdown.currentText()
        if hasattr(self, 'backend') and self.backend.client_socket:
            self.backend.client_socket.close()
        self.backend = ClientBackend("config.json")
        self.backend.connect(self.port)
        self.game_screen()

    def validate_username(self, username):
        return (username.isalnum() and 
                any(char.isupper() for char in username) and 
                any(char.isdigit() for char in username))

    def game_screen(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        outermost_grid = QGridLayout(central_widget)

        self.gamewindow = QGridLayout()
        blank = QGridLayout()
        self.col_indicator = QGridLayout()
        self.row_indicator = QGridLayout()

        self.game_board = QGridLayout()
        self.gamewindow.addLayout(blank, 0, 0)
        self.gamewindow.addLayout(self.col_indicator, 0, 1)
        self.gamewindow.addLayout(self.row_indicator, 1, 0)
        self.gamewindow.addLayout(self.game_board, 1, 1)
        
        button_board = QGridLayout()
        time_left_layout = QVBoxLayout()
        countdown_label = QLabel("Tiempo: ", self)
        self.timer_label = QLabel("00:00", self)
        time_left_layout.addWidget(countdown_label)
        time_left_layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.time_remaining = TIEMPO_JUEGO
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.sandia_timer = QTimer(self)
        self.sandia_timer.timeout.connect(self.spawn_sandia)
        self.sandia_timer.start(TIEMPO_APARICION * 1000)

        check_button = QPushButton("Comprobar", self)
        check_button.clicked.connect(self.validate_solution)
        self.pause_button = QPushButton("Pausar", self)
        self.pause_button.clicked.connect(self.pause_game)
        exit_button = QPushButton("Salir", self)
        exit_button.clicked.connect(self.close)
        button_board.addLayout(time_left_layout, 0, 0)
        button_board.addWidget(check_button, 2, 0)
        button_board.addWidget(self.pause_button, 3, 0)
        button_board.addWidget(exit_button, 4, 0)

        outermost_grid.addLayout(self.gamewindow, 0, 0)
        outermost_grid.addLayout(button_board, 0, 1)

        self.load_board(f"assets/base_puzzles/{self.puzzle}")

    def connectBoardToGridLayout(self, board, row_indicator, col_indicator, game_board):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(1)
        n = board.getHeight()
        m = board.getWidth()

        for i in range(n):
            row_text = board.p_left_list[i]
            row_widget = QWidget(self)
            row_layout = QHBoxLayout(row_widget)
            for num in row_text:
                row_label = QLabel(str(num), self)
                row_layout.addWidget(row_label)
            self.row_indicator.addWidget(row_widget, i, 0)

        for i in range(m):
            col_text = board.p_up_list[i]
            col_widget = QWidget(self)
            col_layout = QVBoxLayout(col_widget)
            for num in col_text:
                col_label = QLabel(str(num), self)
                col_layout.addWidget(col_label)
            self.col_indicator.addWidget(col_widget, 0, i)

        for i in range(n):
            for j in range(m):
                cell = QLabel(self)
                cell.setFixedSize(CELL_SIZE, CELL_SIZE)
                cell.setStyleSheet("border: 0px solid black;")
                cell.setPixmap(QPixmap("assets/sprites/lechuga.png"))
                cell.setScaledContents(True)
                game_board.addWidget(cell, i, j)

    def pause_game(self):
        if self.timer.isActive():
            self.timer.stop()
            self.sandia_timer.stop()
            self.pause_button.setText("Reanudar")
        else:
            self.timer.start(1000)
            self.sandia_timer.start(TIEMPO_APARICION * 1000)
            self.pause_button.setText("Pausar")

    def validate_solution(self):
        self.stop_timers()
        solution = "\n".join(["".join(map(str, row)) for row in self.board.grid])
        response = self.backend.send_message(solution)
        if response == "OK":
            self.play_sound("juego_ganado.wav")
            self.show_message("Solución correcta")
            self.save_score()
        else:
            self.show_message("Solución incorrecta")

    def save_score(self):
        if hasattr(self, 'infinite_time') and self.infinite_time:
            score = PUNTAJE_INF
        else:
            score = (self.time_remaining * self.board.getHeight() * self.board.getWidth() * CONSTANTE) / (300 - self.time_remaining)
        score_entry = f"{self.username}: {round(score, 2)}"
        with open("puntaje.txt", "a") as file:
            file.write(f"{score_entry}\n")
        self.start_screen()

    def update_timer(self):
        if not hasattr(self, 'infinite_time') or not self.infinite_time:
            self.time_remaining -= 1
            minutes, seconds = divmod(self.time_remaining, 60)
            if hasattr(self, 'timer_label') and self.timer_label:
                self.timer_label.setText(f"{minutes:02}:{seconds:02}")
            if self.time_remaining <= 0:
                self.play_sound("juego_perdido.wav")
                self.show_message("Tiempo agotado")
                self.start_screen()

    def show_message(self, message):
        self.stop_timers()
        # Crear un nuevo layout para mostrar el mensaje
        message_layout = QVBoxLayout()
        message_layout.addWidget(QLabel(message, self))
        back_button = QPushButton("Volver a Inicio", self)
        back_button.clicked.connect(self.start_screen)
        message_layout.addWidget(back_button)
        
        # Crear un widget para contener el layout del mensaje
        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        
        # Establecer el widget del mensaje como el central
        self.setCentralWidget(message_widget)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def keyPressEvent(self, event):
        key = event.text().upper()
        if key in ['I', 'N', 'F', 'M', 'U', 'T', 'E']:
            self.cheat_buffer.append(key)
            self.cheat_buffer = self.cheat_buffer[-4:]
            self.check_cheat_codes()
        else:
            if event.key() == Qt.Key.Key_W:
                self.controller.moveUp()
            elif event.key() == Qt.Key.Key_A:
                self.controller.moveLeft()
            elif event.key() == Qt.Key.Key_S:
                self.controller.moveDown()
            elif event.key() == Qt.Key.Key_D:
                self.controller.moveRight()
            elif event.key() == Qt.Key.Key_G:
                self.controller.eat_or_poop()

    def check_cheat_codes(self):
        for code, action in self.cheat_codes.items():
            if ''.join(self.cheat_buffer[-len(code):]) == code:
                action()

    def activate_infinite_time(self):
        self.infinite_time = True
        self.time_remaining = 9999  
        self.timer_label.setText("∞")

    def mute_sounds(self):
        self.muted = True

    def spawn_sandia(self):
        sandia = Sandia(self, self)
        x = random.randint(50, self.width() - 90)
        y = random.randint(50, self.height() - 140)
        sandia.setGeometry(QRect(x, y, 40, 40))
        QTimer.singleShot(TIEMPO_DURACION * 1000, lambda: self.remove_sandia(sandia))

    def remove_sandia(self, sandia):
        if sandia in self.findChildren(Sandia):
            sandia.deleteLater()

    def capture_sandia(self, sandia):
        self.play_sound("sandia.wav")
        self.time_remaining += TIEMPO_ADICIONAL
        self.remove_sandia(sandia)

    def stop_timers(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        if hasattr(self, 'sandia_timer') and self.sandia_timer.isActive():
            self.sandia_timer.stop()
