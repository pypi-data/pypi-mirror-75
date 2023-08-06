def sum(a, b):
    return a + b

def command(args = None):
    if args:
        print("Called with args: ", args)
    else:
        print("Called without args")
