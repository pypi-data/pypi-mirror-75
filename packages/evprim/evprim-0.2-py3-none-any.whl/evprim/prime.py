def errorFloat(x):
    if type(x) == float:
        raise Exception("Float data is not allowed")

def isaprime(x):

    errorFloat(x)
    accountant = 0
    for i in range(2,10):

        if x <= 0 or x == 1:
            accountant+=1
            break

        elif x == i:
            continue

        elif x % i == 0:
            accountant+=1

    if accountant >= 1:
        return False

    else:
        return True
        
def lituPrime(x):
    
    def operation_list():
        list_prime = [] 
        for i in x:
            num = i

            accountant = 0

            for j in range(2, 10):
                
                if num <= 0 or num == 1 or type(num) == float:
                    accountant+=1
                    break

                elif (num) == j:
                    continue

                elif (num) % j == 0:
                    accountant+=1

            if accountant == 0:
                list_prime.append(num)
        
        return list_prime

    if type(x) == list:
        
        return operation_list()

    elif type(x) == tuple:

        tuple_prime = operation_list()
        return tuple(tuple_prime)

    elif type(x) == int:
        raise Exception("Numbers are not allowed without a list or tuple")

def groupPrime(*args):

    tuple_result = []
    for i in args:
        num = i
        accountant = 0

        for j in range(2, 10):

            if num <= 0 or num == 1 or type(num) == float:
                accountant+=1
                break

            elif (num) == j:
                continue

            elif (num) % j == 0:
                accountant+=1

        if accountant == 0:
            tuple_result.append(num)

    if len(tuple_result) == 0:
        return False

    else:
        if len(tuple_result) == 1:
            for i in tuple_result:
                uni_result = i

            return uni_result

        else:    
            return tuple_result
