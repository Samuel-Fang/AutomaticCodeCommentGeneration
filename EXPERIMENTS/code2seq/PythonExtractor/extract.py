import argparse
import re
import json
import multiprocessing
import itertools
import tqdm
import joblib
import numpy as np

from pathlib import Path
from sklearn import model_selection as sklearn_model_selection

import sys
import io



METHOD_NAME, NUM = 'METHODNAME', 'NUM'

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', required=True, type=str)
parser.add_argument('--valid_p', type=float, default=0.2)
parser.add_argument('--max_path_length', type=int, default=8)
parser.add_argument('--max_path_width', type=int, default=2)
parser.add_argument('--use_method_name', type=bool, default=True)
parser.add_argument('--use_nums', type=bool, default=True)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--n_jobs', type=int, default=multiprocessing.cpu_count())
parser.add_argument('--seed', type=int, default=239)


def __collect_asts(json_file):
    asts = []
    with open(json_file, 'r', encoding='utf-8') as f:
        for line in f:
            ast = json.loads(line.strip())
            asts.append(ast)

    return asts


def __terminals(ast, node_index, args):
    stack, paths = [], []

    def dfs(v):
        stack.append(v)

        v_node = ast[v]

        if 'value' in v_node:
            if v == node_index:  # Top-level func def node.
                if args.use_method_name:
                    paths.append((stack.copy(), v_node['value']))
            else:
                v_type = v_node['type']

                if v_type.startswith('Name'):
                    paths.append((stack.copy(), v_node['value']))
                elif args.use_nums and v_type == 'Num':
                    paths.append((stack.copy(), NUM))
                else:
                    pass

        if 'children' in v_node:
            for child in v_node['children']:
                dfs(child)

        stack.pop()

    dfs(node_index)

    return paths


def __merge_terminals2_paths(v_path, u_path):
    s, n, m = 0, len(v_path), len(u_path)
    while s < min(n, m) and v_path[s] == u_path[s]:
        s += 1

    prefix = list(reversed(v_path[s:]))
    lca = v_path[s - 1]
    suffix = u_path[s:]

    return prefix, lca, suffix


def __raw_tree_paths(ast, node_index, args):
    tnodes = __terminals(ast, node_index, args)

    tree_paths = []
    for (v_path, v_value), (u_path, u_value) in itertools.combinations(
            iterable=tnodes,
            r=2,
    ):
        prefix, lca, suffix = __merge_terminals2_paths(v_path, u_path)
        if (len(prefix) + 1 + len(suffix) <= args.max_path_length) \
                and (abs(len(prefix) - len(suffix)) <= args.max_path_width):
            path = prefix + [lca] + suffix
            tree_path = v_value, path, u_value
            tree_paths.append(tree_path)

    return tree_paths


def __delim_name(name):
    if name in {METHOD_NAME, NUM}:
        return name

    def camel_case_split(identifier):
        matches = re.finditer(
            '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
            identifier,
        )
        return [m.group(0) for m in matches]

    blocks = []
    for underscore_block in name.split('_'):
        blocks.extend(camel_case_split(underscore_block))

    return '|'.join(block.lower() for block in blocks)

def __target_name(name):
    if name in {METHOD_NAME, NUM}:
        return name
    
    name = name.replace('-', ' ')
    name = name.replace('_', ' ')
    name = name.replace('.', '')
    name = name.replace('`', '')
    name = name.replace('\'', '')
    splits = name.split()

    if len(splits)>20:
        return None
    else:
        return '|'.join(split.lower() for split in splits)


def __collect_sample(ast, fd_index, args):
    root = ast[fd_index]
    if root['type'] != 'FunctionDef':
        raise ValueError('Wrong node type.')

    #target = root['value']

    tree_paths = __raw_tree_paths(ast, fd_index, args)
    contexts = []
    for tree_path in tree_paths:
        start, connector, finish = tree_path

        start, finish = __delim_name(start), __delim_name(finish)
        connector = '|'.join(ast[v]['type'] for v in connector)

        context = f'{start},{connector},{finish}'
        contexts.append(context)

    if len(contexts) == 0:
        return None

    #target = __delim_name(target)
    context = ' '.join(contexts)

    #return f'{target} {context}'
    return context


def __collect_samples(ast, args):
    samples = []
    funcFirst = True
    tarFirst = True
    sampleAdded = False
    TooLong = False
    for node_index, node in enumerate(ast):
        if node['type'] == 'FunctionDef' and funcFirst:
            sample_context = __collect_sample(ast, node_index, args)
            if sample_context is not None:
                funcFirst = False
                #samples.append(sample)
        if (node['type'] == 'Expr') and (len(node['children']) == 1) and tarFirst:                
            target_index = node['children'][0]
            if ast[target_index]['type'] == 'Constant':
                tarFirst = False
                target = __target_name(ast[target_index]['value'].strip())
                if target is None: TooLong = True
        if (not funcFirst) and (not tarFirst) and (not sampleAdded) and (not TooLong):
            sample = f'{target} {sample_context}'
            samples.append(sample)
            sampleAdded = True
                

    return samples


def __collect_all_and_save(asts, args, output_file):
    parallel = joblib.Parallel(n_jobs=args.n_jobs)
    func = joblib.delayed(__collect_samples)

    samples = parallel(func(ast, args) for ast in tqdm.tqdm(asts))
    samples = list(itertools.chain.from_iterable(samples))

    with open(output_file, 'w', encoding='utf-8') as f:
        for line_index, line in enumerate(samples):
            f.write(line + ('' if line_index == len(samples) - 1 else '\n'))


def main():
    #sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    #sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

    args = parser.parse_args()
    np.random.seed(args.seed)

    data_dir = Path(args.data_dir)
    train = __collect_asts(data_dir / 'train_ast.json')
    test = __collect_asts(data_dir / 'test_ast.json')
    valid = __collect_asts(data_dir / 'valid_ast.json')

    #train, valid = sklearn_model_selection.train_test_split(
    #   trains,
    #   test_size=args.valid_p,
    #)
    #test = evals

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    for split_name, split in zip(
            ('train', 'valid', 'test'),
            (train, valid, test),
    ):
        output_file = output_dir / f'{split_name}_output_file.txt'
        __collect_all_and_save(split, args, output_file)


if __name__ == '__main__':
    main()
