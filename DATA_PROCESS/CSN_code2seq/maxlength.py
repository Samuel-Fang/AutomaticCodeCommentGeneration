import json
import xlwt
import matplotlib.pyplot as plt

inputfile = 'train_target_finish.json'
#of = xlwt.Workbook()
#sheet1 = of.add_sheet('length')

with open(inputfile, 'r') as f:
    maxlen = 0
    index = 0
    tlens = []
    sum = 0
    for line in f:
        jsonline = json.loads(line.strip())['docstring']
        splits = jsonline.split('|')
        tlen = len(splits)
        tlens.append(tlen)
        sum = sum + tlen
        if tlen > maxlen: maxlen = tlen
        #sheet1.write(index, 0, tlen)
        index+=1

print(maxlen)
print(sum/len(tlens))
#of.save('length.xlsx')
plt.hist(tlens)
plt.show()