# core_language.py
class LanguageInterpreter:
    def __init__(self):
        self.environment = {}
    
    def parse(self, code: str):
        # Basic parsing logic for the second-layer language
        lines = code.splitlines()
        parsed = []
        for line in lines:
            command, *args = line.split()
            parsed.append((command, args))
        return parsed

    def execute(self, parsed_code):
        for command, args in parsed_code:
            self.dispatch_command(command, args)
    
    def dispatch_command(self, command, args):
        # Basic command dispatch logic
        if command == "PRINT":
            print(" ".join(args))
        elif command == "SET":
            var_name = args[0]
            value = " ".join(args[1:])
            self.environment[var_name] = value
        else:
            print(f"Unknown command: {command}")
