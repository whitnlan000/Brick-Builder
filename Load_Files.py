import os
def find_file(file):
    return os.getcwd() + "\Levels\lvl_"+str(file)+".txt"

def load(file):
    blocks = []
    for x in range(9):
        for y in range(8):
            if open(file).read().splitlines()[x][y] == '1':
                blocks.append((x,y))
                print(x,y)

    return blocks
