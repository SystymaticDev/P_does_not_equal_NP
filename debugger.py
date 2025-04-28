class Debugger:
    def __init__(self):
        self.breakpoints = set()

    def add_breakpoint(self, line_number):
        self.breakpoints.add(line_number)

    def remove_breakpoint(self, line_number):
        self.breakpoints.discard(line_number)

    def clear_breakpoints(self):
        self.breakpoints.clear()

    def step_over(self):
        # Stub for stepping over a line in the debugger
        pass

    def step_into(self):
        # Stub for stepping into a function call
        pass

    def step_out(self):
        # Stub for stepping out of the current function
        pass
