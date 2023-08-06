def isreal(x):
    if isinstance(x, float):
        return True
    elif isinstance(x, int):
        return True
    elif isinstance(x, str):
        if x.isnumeric():
            return True
        else:
            return False
    else:
        return False
