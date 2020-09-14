import json

file_name = 'python_test_0.jsonl'
output_file = 'code.txt'
of = open(output_file, 'a')

with open(file_name, 'r') as f:
    for line in f:
        jsonline = json.loads(line.strip())
        if jsonline['func_name']=='DAGCircuit.remove_ancestors_of':
            of.write(jsonline['code'])
