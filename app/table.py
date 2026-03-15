from app.parser import tree
from app.node import Node, Var, Not, And, Or, Implies, Bincon
import itertools
import re

def gen_comb(variables):
    return list(itertools.product([True, False], repeat = len(variables)))

def get_subformulas(node, subs=None, ops=None):

    if subs is None:
        subs = []

    if ops is None:
        ops = []

    if isinstance(node, Var):
        return node.name

    if isinstance(node, Not):
        child = get_subformulas(node.child, subs, ops)
        expr = "~" + child
        subs.append(expr)
        ops.append(node)
        return expr

    left = get_subformulas(node.left, subs, ops)
    right = get_subformulas(node.right, subs, ops)


    expr = f"({left} {str(node)} {right})"

    subs.append(expr)
    ops.append(node)

    return expr

def print_table(tabla):

    widths = [max(len(str(row[i])) for row in tabla) for i in range(len(tabla[0]))]
    ret = ""

    for row in tabla:
        fila = " | ".join(str(val).center(widths[i]) for i, val in enumerate(row))
        ret += fila + "\n"

    return ret

def truth_table(expr: str):

    prim = sorted(set(re.findall(r"[A-Za-z]", expr)))
    n = len(prim)

    root = tree(expr)

    col = prim.copy()
    ops = []
    get_subformulas(root, col, ops)
    col = [col]

    for values in itertools.product([True, False], repeat = n):
        row = []
        context = {}

        for i in range(n):
            if values[i]:
                row.append(1)
            else:
                row.append(0)
            context[prim[i]] = values[i]

        for node in ops:
            if node.evaluate(context):
                row.append(1)
            else:
                row.append(0)

        col.append(row)

    return print_table(col)
