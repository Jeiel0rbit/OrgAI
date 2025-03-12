import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QLabel, QProgressBar, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QTimer, Qt

# Função para obter o caminho correto do recurso (compatível com PyInstaller)
def get_resource_path(relative_path):
    """ Retorna o caminho do recurso, funcionando tanto no modo normal quanto no PyInstaller """
    if getattr(sys, 'frozen', False):  # Se estiver rodando como .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

# Classe personalizada para efeito de clique (efeito cascata)
class MyButton(QPushButton):
    def __init__(self, text="", default_style="", pressed_style=""):
        super().__init__(text)
        self.default_style = default_style
        self.pressed_style = pressed_style
        self.setStyleSheet(self.default_style)
    
    def mousePressEvent(self, event):
        self.setStyleSheet(self.pressed_style)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        QTimer.singleShot(100, lambda: self.setStyleSheet(self.default_style))
        super().mouseReleaseEvent(event)

# Classe principal do aplicativo
class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("OrgAI")
        self.setWindowIcon(QIcon(get_resource_path("logo.ico")))  # Usa a função para encontrar o ícone
        self.setFixedSize(300, 250)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            color: #333;
        """)

        layout = QVBoxLayout()
        
        # Layout superior para o botão "Sobre"
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.about_button = MyButton(
            "Sobre",
            default_style="background-color: transparent; border: none; color: #333; font-size: 10px;",
            pressed_style="background-color: #ddd; border: none; color: #333; font-size: 10px;"
        )
        self.about_button.setFixedSize(50, 30)
        self.about_button.clicked.connect(self.show_about_dialog)
        top_layout.addWidget(self.about_button)
        layout.addLayout(top_layout)

        # Rótulo de instrução
        self.label = QLabel("Selecione uma pasta \npara organizar os arquivos.")
        self.label.setFont(QFont("Arial", 12))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Botão para selecionar pasta
        self.select_btn = MyButton(
            "Selecionar Pasta",
            default_style="background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 5px;",
            pressed_style="background-color: #45a049; color: white; font-size: 14px; padding: 10px; border-radius: 5px;"
        )
        self.select_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_btn)

        # Botão para organizar arquivos (inicialmente oculto)
        self.organize_btn = MyButton(
            "Organizar Arquivos",
            default_style="background-color: #008CBA; color: white; font-size: 14px; padding: 10px; border-radius: 5px;",
            pressed_style="background-color: #007bb5; color: white; font-size: 14px; padding: 10px; border-radius: 5px;"
        )
        self.organize_btn.clicked.connect(self.organize_files)
        self.organize_btn.setVisible(False)
        layout.addWidget(self.organize_btn)

        # Barra de progresso (inicialmente oculta)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def show_about_dialog(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("Sobre")
        about_dialog.setText("OrgAI\nVersão 1.0\nDesenvolvido por Jeiel Miranda.")
        about_dialog.setStyleSheet("""
            QMessageBox { background-color: #f0f0f0; color: #333; font-size: 14px; }
            QMessageBox QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px; }
            QMessageBox QPushButton:hover { background-color: #45a049; }
        """)
        about_dialog.exec()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecione a Pasta")
        if folder:
            self.label.setText(f"Pasta Selecionada:\n{folder}")
            self.folder_path = folder
            self.organize_btn.setVisible(True)

    def organize_files(self):
        if not hasattr(self, 'folder_path'):
            self.label.setText("Selecione uma pasta primeiro!")
            return

        try:
            files = [
                f for f in os.listdir(self.folder_path)
                if os.path.isfile(os.path.join(self.folder_path, f))
            ]
            if not files:
                self.label.setText("Nenhum arquivo para organizar.")
                return

            self.progress_bar.setMaximum(len(files))
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)

            for i, file in enumerate(files):
                file_path = os.path.join(self.folder_path, file)
                ext = file.split(".")[-1].upper()
                dest_folder = os.path.join(self.folder_path, ext + "_FILES")

                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder, exist_ok=True)
                if os.path.exists(file_path):
                    shutil.move(file_path, os.path.join(dest_folder, file))

                self.progress_bar.setValue(i + 1)
                QApplication.processEvents()

            self.label.setText("Organização Concluída!")
            QTimer.singleShot(1500, lambda: self.progress_bar.setVisible(False))

        except Exception as e:
            self.label.setText(f"Ocorreu um erro: {str(e)}")
            print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())