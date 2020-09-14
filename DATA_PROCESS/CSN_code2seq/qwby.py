data1 = [1,2,3,4]
data2 = [5,6,7,8]

for (i, j) in zip(data1, data2):
    print(i+j)

s = 'train0'

print(s[:5])

with open('./test/python_test_0.jsonl', 'r') as f:
    lines = f.readlines()
    print(lines[0])