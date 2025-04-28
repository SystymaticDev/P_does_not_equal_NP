# builtin_functions.py
def loop(times, function):
    for _ in range(times):
        function()

def condition(test, true_block, false_block=None):
    if test():
        true_block()
    elif false_block:
        false_block()

def standard_print(*args):
    print(*args)
