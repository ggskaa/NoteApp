import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QDialog, QLineEdit, QLabel, QFormLayout, QDialogButtonBox,
    QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent

from utils import create_note, delete_note, all_notes, change_note_content


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)

        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #1e1e2f, stop:1 #16213e);
            color: white;
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        self.title = QLabel("📝 Notes App")
        self.title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.title)
        layout.addStretch()

        btn_min = QPushButton("─")
        btn_min.clicked.connect(self.parent.showMinimized)
        btn_max = QPushButton("⬜")
        btn_max.clicked.connect(self.toggle_max_restore)
        btn_close = QPushButton("✕")
        btn_close.clicked.connect(self.parent.close)

        for btn in (btn_min, btn_max, btn_close):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    color: #e2e8f0;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 6px;
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.2);
                }
            """)
            layout.addWidget(btn)

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

        layout = QFormLayout()

        self.setWindowTitle("Create Note")
        self.setFixedSize(400, 250)

        self.title_input = QLineEdit()
        self.content_input = QLineEdit()

        layout.addRow(QLabel("Title:"), self.title_input)
        layout.addRow(QLabel("Content:"), self.content_input)

        buttons = QDialogButtonBox()
        btn_ok = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        buttons.addButton(btn_ok, QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(btn_cancel, QDialogButtonBox.ButtonRole.RejectRole)

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        layout.addRow(buttons)
        self.setLayout(layout)

    def get_data(self):
        return self.title_input.text(), self.content_input.text()


class DisplayNote(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()


        self.note = note
        self.main_window = parent
        # CustomTitleBar(self)
        # self.setWindowTitle(f"{note.title}, -> ID:{note.id}")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(800, 400) # => пока-что коректно только в фул-сайз моде

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

        # убираем стандартный title bar
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

        # === ВСТАВЛЯЕМ КАСТОМНЫЙ TITLE BAR ===
        self.title_bar = CustomTitleBar(self)
        layout.addWidget(self.title_bar)

        # === Всё остальное как у тебя ===
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
            btn = QPushButton(f"📝 {note.id} - {note.title}")
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
