import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QDialog, QLineEdit, QLabel, QFormLayout, QDialogButtonBox,
    QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QFont

from utils import create_note, delete_note, all_notes, change_note_content


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.dragPos = QPoint()

        self.setStyleSheet("""
            CustomTitleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #1e1e2f, stop:1 #16213e);
                border-bottom: 2px solid rgba(99, 102, 241, 0.3);
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)

        layout.addStretch()

        # Центральный логотип
        self.title = QLabel("                                  Notes App")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("""
            QLabel {
                color: #f1f5f9;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        layout.addStretch()

        btn_min = QPushButton("─")
        btn_min.clicked.connect(self.parent.showMinimized)
        btn_max = QPushButton("☐")
        btn_max.clicked.connect(self.toggle_max_restore)
        btn_close = QPushButton("✕")
        btn_close.clicked.connect(self.parent.close)

        # Стили для кнопок управления
        button_style = """
            QPushButton {
                border: none;
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                min-width: 35px;
                min-height: 35px;
                max-width: 35px;
                max-height: 35px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                color: #ffffff;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.25);
            }
        """

        close_button_style = """
            QPushButton {
                border: none;
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
                background: rgba(239, 68, 68, 0.2);
                border-radius: 8px;
                min-width: 35px;
                min-height: 35px;
                max-width: 35px;
                max-height: 35px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.4);
                color: #ffffff;
            }
            QPushButton:pressed {
                background: rgba(239, 68, 68, 0.6);
            }
        """

        btn_min.setStyleSheet(button_style)
        btn_max.setStyleSheet(button_style)
        btn_close.setStyleSheet(close_button_style)

        layout.addWidget(btn_min)
        layout.addWidget(btn_max)
        layout.addWidget(btn_close)

        self.setLayout(layout)

    def toggle_max_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.parent.move(self.parent.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()


class AddNote(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 350)

        # Стили для диалога создания заметки
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #1a1a2e, stop:1 #16213e);
                border: 2px solid rgba(99, 102, 241, 0.3);
                border-radius: 20px;
            }
            
            QLabel {
                color: #f1f5f9;
                font-size: 16px;
                font-weight: 600;
                font-family: "Segoe UI", "Roboto", "Inter";
                margin-bottom: 8px;
            }

            QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 15px;
                color: #f8fafc;
                font-size: 14px;
                font-family: "Segoe UI", "Roboto", "Inter";
                min-height: 20px;
            }

            QLineEdit:focus {
                border: 2px solid #6366f1;
                background: rgba(255, 255, 255, 0.12);
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
            }

            QPushButton {
                font-size: 15px;
                font-weight: 600;
                font-family: "Segoe UI", "Roboto", "Inter";
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #3b82f6, stop:1 #2563eb);
                border: none;
                border-radius: 12px;
                color: white;
                padding: 12px 24px;
                min-height: 45px;
                margin: 5px;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #2563eb, stop:1 #1d4ed8);
                transform: translateY(-1px);
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #1d4ed8, stop:1 #1e40af);
            }
            
            QPushButton#cancelBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #64748b, stop:1 #475569);
            }
            
            QPushButton#cancelBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #475569, stop:1 #334155);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title_label = QLabel(" Create New Note")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #f1f5f9; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title...")
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Enter note content...")

        form_layout.addRow(QLabel("Title:"), self.title_input)
        form_layout.addRow(QLabel("Content:"), self.content_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("cancelBtn")
        btn_ok = QPushButton("Save")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_ok)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_data(self):
        return self.title_input.text(), self.content_input.text()


class DisplayNote(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.note = note
        self.main_window = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(800, 400)

        self.content_edit = QTextEdit(note.content)

        button_row = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_close = QPushButton("Close")
        btn_delete = QPushButton("Delete")

        btn_save.clicked.connect(self.save_note)
        btn_close.clicked.connect(self.close)
        btn_delete.clicked.connect(self.delete_note)

        button_row.addWidget(btn_save)
        button_row.addWidget(btn_close)
        button_row.addWidget(btn_delete)

        layout.addWidget(self.content_edit)
        layout.addLayout(button_row)
        self.setLayout(layout)

    def delete_note(self):
        delete_note(self.note.id)
        self.accept()
        self.main_window.view_all_notes()

    def save_note(self):
        new_content = self.content_edit.toPlainText()
        change_note_content(self.note.id, new_content)
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1600, 900)

        # =========! style made by GPT !==========
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #0f172a, stop:1 #1e293b);
            }

            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #1a1a2e, stop:1 #16213e);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }

            QLabel {
                color: #f1f5f9;
                font-size: 14px;
                font-weight: 500;
                font-family: "Segoe UI", "Roboto", "Inter";
            }

            QLineEdit, QTextEdit {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 10px;
                color: #f8fafc;
                font-size: 14px;
                font-family: "Segoe UI", "Roboto", "Inter";
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #6366f1;
                background: rgba(255, 255, 255, 0.1);
            }

            QPushButton {
                font-size: 14px;
                font-family: "Segoe UI", "Roboto", "Inter";
                background: #3b82f6;
                border-radius: 10px;
                color: white;
                padding: 10px 16px;
            }

            QPushButton:hover {
                background: #2563eb;
            }

            QPushButton:pressed {
                background: #1d4ed8;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        layout.addWidget(self.title_bar)

        main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(20, 20, 20, 20)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(10)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        btn_create_note = QPushButton("Create Note")
        btn_create_note.clicked.connect(self.create_note)

        btn_all_notes = QPushButton("All Notes")
        btn_all_notes.clicked.connect(self.view_all_notes)

        for btn in (btn_create_note, btn_all_notes):
            btn.setFixedHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.left_layout.addWidget(btn)
        self.left_layout.addStretch()

        main_layout.addLayout(self.left_layout, 1)
        main_layout.addLayout(self.right_layout, 3)

        wrapper = QWidget()
        wrapper.setLayout(main_layout)
        layout.addWidget(wrapper)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def create_note(self):
        add_dialog = AddNote()
        if add_dialog.exec():
            title, content = add_dialog.get_data()
            note = create_note(title, content)
            self.view_all_notes()
            print("Created:", note)

    def view_all_notes(self):
        self.clear_layout(self.right_layout)
        notes = all_notes()
        for note in notes:
            btn = QPushButton(f" {note.id} - {note.title}")
            btn.clicked.connect(lambda checked=False, n=note: self.open_note_window(n))
            btn.setFixedHeight(40)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.right_layout.addWidget(btn)
        self.right_layout.addStretch()

    def open_note_window(self, note):
        dialog = DisplayNote(note, self)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()