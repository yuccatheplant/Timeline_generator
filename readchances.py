import random

def readChances(chances):
    chance = random.random()
    result = 0
    for i in chances:
        if chance <= i[0]:
            result = i[1]
        else:
            break
    
    return result