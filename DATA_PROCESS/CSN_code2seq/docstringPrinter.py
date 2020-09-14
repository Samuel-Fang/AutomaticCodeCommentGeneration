import json

f = open('test/python_test_0.jsonl', 'r', encoding='utf-8')
of = open('printedDocstrings.txt', 'a')
for line in f:
    fuc = json.loads(line.strip())
    of.write(fuc['docstring']+'\n')
    of.write('------------------check-------------------\n')