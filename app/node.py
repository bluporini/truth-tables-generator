class Node:
    def evaluate(self, context):
        raise NotImplementedError()


class Var(Node):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, context):
        return context[self.name]


class Not(Node):

    def __init__(self, child):
        self.child = child

    def __str__(self):
        return "~"

    def evaluate(self, context):
        return (not self.child.evaluate(context))


class And(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "∧"

    def evaluate(self, context):
        return self.left.evaluate(context) and self.right.evaluate(context)


class Or(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "∨"

    def evaluate(self, context):
        return self.left.evaluate(context) or self.right.evaluate(context)


class Implies(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "->"

    def evaluate(self, context):
        return (not self.left.evaluate(context)) or self.right.evaluate(context)
    

class Bincon(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "<->"

    def evaluate(self, context):
        return ((not self.left.evaluate(context)) or self.right.evaluate(context)) \
                and ((not self.right.evaluate(context)) or self.left.evaluate(context))