import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, 
    QFileDialog, QPushButton, QHBoxLayout, QLabel, QTextEdit
)
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QPainter
from PyQt5.QtCore import Qt, QRect

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return self.editor.lineNumberAreaWidth(), 0

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class SyntaxHighlighter:
    def __init__(self, editor):
        self.editor = editor
        self.setup_rules()

    def setup_rules(self):
        self.rules = []
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keywords = [
            "def", "class", "if", "else", "elif", "for", "while", "return",
            "import", "from", "as", "try", "except", "finally", "with", "yield",
            "assert", "del", "global", "nonlocal", "pass", "raise"
        ]
        for keyword in keywords:
            self.rules.append((keyword, keyword_format))

    def highlight(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.Start)
        document = self.editor.document()
        block_count = document.blockCount()
        for i in range(block_count):
            block = document.findBlockByNumber(i)
            block_text = block.text()
            for pattern, fmt in self.rules:
                start_idx = block_text.find(pattern)
                if start_idx >= 0:
                    cursor.setPosition(block.position() + start_idx)
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(pattern))
                    cursor.mergeCharFormat(fmt)

class PlangEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.highlighter = SyntaxHighlighter(self)
        self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        return 3 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extra_selections = []
        selection = QTextEdit.ExtraSelection()

        line_color = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(line_color)
        selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                rect = QRect(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height())
                painter.setPen(Qt.black)
                painter.drawText(rect, Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

class PlangIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plang IDE")
        self.setGeometry(100, 100, 800, 600)

        # Set up main editor where user writes code
        self.editor = PlangEditor(self)
        self.editor.setFont(QFont("Courier", 10))

        # Set up output console for showing run results or debug logs
        self.output_console = QTextEdit(self)
        self.output_console.setReadOnly(True)

        # Run button to execute the code
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_code)

        # Open and Save buttons for file management
        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_file)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_file)

        # Setup UI layout
        self.setup_layout()

    def setup_layout(self):
        """
        Defines the layout of the main window including editor, buttons, and console.
        """
        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.open_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.run_button)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(QLabel("Code Editor:"))
        main_layout.addWidget(self.editor)
        main_layout.addWidget(QLabel("Console Output:"))
        main_layout.addWidget(self.output_console)

        # Create a central widget to hold the layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_file(self):
        """
        Opens a file dialog to select and read a Python file into the editor.
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Python File", "", "Python Files (*.py)"
        )
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    self.editor.setPlainText(file.read())
            except Exception as e:
                self.output_console.append(f"Error opening file: {e}")

    def save_file(self):
        """
        Opens a file dialog to select a path and saves the editor content to that file.
        """
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Python File", "", "Python Files (*.py)"
        )
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    file.write(self.editor.toPlainText())
                self.output_console.append("File saved successfully.")
            except Exception as e:
                self.output_console.append(f"Error saving file: {e}")

    def run_code(self):
        """
        Executes the code entered in the editor and prints the output in the console.
        """
        code = self.editor.toPlainText()
        self.output_console.clear()
        self.output_console.append("---- Running Code ----")

        # Redirect stdout and stderr to capture output
        import io
        import contextlib

        output = io.StringIO()
        error = io.StringIO()

        try:
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                exec(code, {})
            self.output_console.append(output.getvalue())
        except Exception as e:
            self.output_console.append(f"Error: {str(e)}")
        finally:
            output.close()
            error.close()

        self.output_console.append("---- Execution Finished ----")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = PlangIDE()
    ide.show()
    sys.exit(app.exec_())
