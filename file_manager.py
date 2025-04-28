from pathlib import Path

class FileManager:
    def __init__(self):
        self.current_file_path = None

    def open_file(self, path):
        self.current_file_path = Path(path)
        with open(path, 'r') as file:
            return file.read()

    def save_file(self, content):
        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(content)

    def save_as(self, path, content):
        self.current_file_path = Path(path)
        self.save_file(content)
