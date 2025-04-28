import subprocess
import sys

class CodeRunner:
    def __init__(self):
        self.current_process = None

    def run_code(self, code):
        """
        Runs the given code string in a subprocess.
        """
        if self.current_process:
            self.stop_running_code()
        
        self.current_process = subprocess.Popen(
            [sys.executable, '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def read_output(self):
        if self.current_process:
            out, err = self.current_process.communicate()
            return out, err

    def stop_running_code(self):
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
