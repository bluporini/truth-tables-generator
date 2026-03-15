import re
from app.node import Node, Var, Not, And, Or, Implies, Bincon

def find_main_operator(token):
    """
    Busca el árbol de precedencia de los operadores lógicos dado un token.
    """

    pos = 1
    aux = 1

    while aux != 0:
        if token[pos] == "(":
            aux += 1
        if token[pos] == ")":
            aux -= 1

        pos +=1
    
    return pos, token[pos]

def remove_outer_parentheses(expr):
    """
    Elimina los paréntesis externos (redundantes).
    """
    
    if expr.startswith("(") and expr.endswith(")"):
        long = len(expr)
        pos = 1
        aux = 1

        while aux != 0 and aux <= long:
            if expr[pos] == "(":
                aux += 1
            if expr[pos] == ")":
                aux -= 1

            pos +=1

        if pos == long:
            expr = expr[1:long-1]

    return expr

def tree(expr:str):
    """
    Retorna la raiz (class) de un árbol donde los nodos intermedios son operadores lógicos y
    las hojas son proposiciones primitivas.
    """

    expr = remove_outer_parentheses(expr)
    tokens = re.findall(r"[A-Za-z]+|->|~|∧|∨|<->|\(|\)", expr)
    long = len(tokens)

    if long == 1:
        return Var(tokens[0])             # Case p
    
    if long == 2:                       # Case ~p
        return Not(Var(tokens[1]))
    
    if long == 3:
        if tokens[1] == "->":
            return Implies(Var(tokens[0]), Var(tokens[2]))    # Case p -> q
        
        elif tokens[1] == "∧":
            return And(Var(tokens[0]), Var(tokens[2]))        # Case p ∧ q
        
        elif tokens[1] == "∨":
            return Or(Var(tokens[0]), Var(tokens[2]))         # Case p ∨ q
        
        elif tokens[1] == "<->":
            return Bincon(Var(tokens[0]), Var(tokens[2]))     # Case p <-> q

    if tokens[0].isalpha():
        if tokens[1] == "->":
            exp2 = "".join(tokens[2:long])
            return Implies(tree(expr[0]), tree(exp2))    # Case p -> Q
        
        elif tokens[1] == "∧":
            exp2 = "".join(tokens[2:long])
            return Implies(tree(expr[0]), tree(exp2))        # Case p ∧ Q
        
        elif tokens[1] == "∨":
            exp2 = "".join(tokens[2:long])
            return Or(tree(expr[0]), tree(exp2))         # Case p ∨ Q
        
        elif tokens[1] == "<->":
            exp2 = "".join(tokens[2:long])
            return Bincon(tree(expr[0]), tree(exp2))     # Case p <-> Q
            
    if tokens[0] == "~":
        if tokens[2] == "->":
            exp1 = "".join(tokens[0:2])
            exp2 = "".join(tokens[3:long])
            return Implies(tree(exp1), tree(exp2))    # Case ~p -> Q
        
        elif tokens[2] == "∧":
            exp1 = "".join(tokens[0:2])
            exp2 = "".join(tokens[3:long])
            return And(tree(exp1), tree(exp2))        # Case ~p ∧ Q
            
        elif tokens[2] == "∨":
            exp1 = "".join(tokens[0:2])
            exp2 = "".join(tokens[3:long])
            return Or(tree(exp1), tree(exp2))         # Case ~p ∨ Q
            
        elif tokens[2] == "<->":
            exp1 = "".join(tokens[0:2])
            exp2 = "".join(tokens[3:long])
            return Bincon(tree(exp1), tree(exp2))     # Case ~p <-> Q
            
    if tokens[long-2] == "~":
        if tokens[long-3] == "->":
            exp1 = "".join(tokens[0:long-3])
            exp2 = "".join(tokens[long-2:long-1])
            return Implies(tree(exp1), tree(exp2))     # Case Q -> ~p
        
        elif tokens[long-3] == "∧":
            exp1 = "".join(tokens[0:long-3])
            exp2 = "".join(tokens[long-2:long-1])
            return And(tree(exp1), tree(exp2))         # Case Q ∧ ~p
            
        elif tokens[long-3] == "∨":
            exp1 = "".join(tokens[0:long-3])
            exp2 = "".join(tokens[long-2:long-1])
            return Or(tree(exp1), tree(exp2))          # Case Q ∨ ~p
            
        elif tokens[long-3] == "<->":
            exp1 = "".join(tokens[0:long-3])
            exp2 = "".join(tokens[long-2:long-1])
            return Bincon(tree(exp1), tree(exp2))      # Case Q <-> ~p
            
    if tokens[long-1].isalpha():
        if tokens[long-2] == "->":
            exp1 = "".join(tokens[0:long-2])
            return Implies(tree(exp1), tree(tokens[long-1]))     # Case Q -> p
        
        elif tokens[long-2] == "∧":
            exp1 = "".join(tokens[0:long-2])
            return And(tree(exp1), tree(tokens[long-1]))         # Case Q ∧ p
            
        elif tokens[long-2] == "∨":
            exp1 = "".join(tokens[0:long-2])
            return Or(tree(exp1), tree(tokens[long-1]))          # Case Q ∨ p
            
        elif tokens[long-2] == "<->":
            exp1 = "".join(tokens[0:long-2])
            return Bincon(tree(exp1), tree(tokens[long-1]))      # Case Q <-> p
            
    [pos, c] = find_main_operator(tokens)
    exp1 = "".join(tokens[0:pos])
    exp2 = "".join(tokens[pos+1:long])

    if c == "->":
        return Implies(tree(exp1), tree(exp2))     # Case P -> Q
        
    elif c == "∧":
        return And(tree(exp1), tree(exp2))        # Case P ∧ Q
            
    elif c == "∨":
        return Or(tree(exp1), tree(exp2))          # Case P ∨ Q
            
    elif c == "<->":
        return Bincon(tree(exp1), tree(exp2))     # Case P <-> Q
            


def _print_tree(node, prefix="", is_last=True):

    """
    Imprimimos en pantalla el árbol generado por la clase 'tree'.
    """

    connector = "└── " if is_last else "├── "
    print(prefix + connector + str(node))

    prefix += "    " if is_last else "│   "

    children = []
    if hasattr(node, "child"):
        children.append(node.child)
    if hasattr(node, "left"):
        children.append(node.left)
    if hasattr(node, "right"):
        children.append(node.right)

    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        _print_tree(child, prefix, is_last_child)
