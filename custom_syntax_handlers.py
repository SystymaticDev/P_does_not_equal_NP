# custom_syntax_handlers.py
class SyntaxHandler:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, keyword, function):
        self.handlers[keyword] = function

    def handle(self, command, *args):
        if command in self.handlers:
            self.handlers[command](*args)
        else:
            raise SyntaxError(f"No handler for keyword: {command}")
