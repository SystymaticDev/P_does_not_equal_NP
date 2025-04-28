# code_generation.py
class CodeGenerator:
    def __init__(self):
        self.generated_code = []
    
    def add_line(self, line):
        self.generated_code.append(line)
    
    def compile(self):
        return "\n".join(self.generated_code)

    def run(self):
        exec(self.compile())

