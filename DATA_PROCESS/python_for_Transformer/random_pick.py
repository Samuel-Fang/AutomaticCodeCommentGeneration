import numpy as np
from random import choice

numbers = list(range(6421))

subtoken_file = './CSNpython/test/code.original_subtoken'
sf = open(subtoken_file)
subtokens = []
for line in sf:
    subtokens.append(line.strip().split())

i = 1
picked = []
while not i>10:
    pick = choice(numbers)
    if not pick+1 in picked and len(subtokens[pick])<512:
        i+=1
        picked.append(pick+1)

print(picked)
