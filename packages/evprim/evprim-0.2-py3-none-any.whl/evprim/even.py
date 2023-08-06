def errorFloat(x):
    if type(x) == float:
        raise Exception("Float data is not allowed")

def isaeven(x):
    errorFloat(x)

    if x % 2 == 0:
        return True
    else:
        return False

def isaodd(x):
    
    errorFloat(x)

    if x % 2 == 0:
        return False

    else:
        return True
