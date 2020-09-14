import json

astFile = 'valid_ast.json'
outputFile = 'v_docstring.txt'

with open(astFile, 'r', encoding='utf-8') as f:
    for line in f:
        ast = json.loads(line.strip())
        first = True
        for node_index, node in enumerate(ast):
            if (node['type'] == 'Expr') and (len(node['children']) == 1) and first:                
                index = node['children'][0]
                if ast[index]['type'] == 'Constant':
                    first = False
                    with open(outputFile, 'a') as of:
                        of.write(ast[index]['value'].strip()+'\n')
                    #print(ast[index]['value'])

                