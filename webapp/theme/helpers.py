import random

def rgb_number():
    r = random.randint(50,255)
    g = random.randint(50,255)
    b = random.randint(50,255)
    rgb_number ='rgb('+str(r)+','+str(g)+','+str(b)+')'
    return rgb_number