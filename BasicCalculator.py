# Calculator.py
# This program uses an expression tree to create a basic integer calculator app.
# 1.Input the expression.
# 2.Extract numbers and operator from input
# 3.Generate Token list. Token has two types: number, and operator.

# Input Processing


class Buffer(object):
    # Constructor

    def __init__(self, data):
        self.data = data
        self.offset = 0      # offset indicates the position in the string

    # Extract the character at position offset
    def peek(self):
        # If the end has been rached, return None
        if self.offset >= len(self.data):
            return None
        return self.data[self.offset]

    # Advance offset one position towards the end
    def advance(self):
        self.offset = self.offset + 1

# Generate Token List


class Token(object):

    def extract(self, buffer):     # Extracts a token from buffer object
        pass


class IntToken(Token):
    # Reads character from string untill it's no longer an integer

    def extract(self, buffer):
        res = ""
        while buffer.peek() != None:
            char = buffer.peek()
            if char not in "0123456789":
                break
            else:
                res = res + char
                buffer.advance()
        if res != "":
            return ("int", int(res))
        else:
            return None


class OperatorToken(Token):
        # Reads character from string and return that character, if it's not
        # operator return None

    def extract(self, buffer):
        char = buffer.peek()
        if char is not None and char in "+-":
            buffer.advance()
            return ("op", char)
        return None


def getToken(string):
    buffer = Buffer(string)
    int_tk = IntToken()
    op_tk = OperatorToken()
    tokens = []

    while buffer.peek():
        token = None
        for tk in (int_tk, op_tk):
            token = tk.extract(buffer)
            if token:
                tokens.append(token)
                break
        if not token:
            raise ValueError("Error in syntax")

    return tokens

# Generate expression tree


class Node(object):
    pass


class IntNode(Node):

    def __init__(self, value):
        self.value = value


class OpNode(Node):

    def __init__(self, kind):
        self.kind = kind
        self.left = None
        self.right = None


def parse(tokens):
    if tokens[0][0] != 'int':
        raise ValueError("Must start with an int")
    # Extract tokens[0] whose type is integer
    node = IntNode(tokens[0][1])
    opnode = None
    kind = tokens[0][0]
    for token in tokens[1:]:
        if token[0] == kind:       # if two neibouring tokens have the same type, it's an error
            raise ValueError("Error in syntax")
        kind = token[0]
        # if current token is an operator, make the previous integer node its
        # left sub tree
        if token[0] == 'op':
            opnode = OpNode(token[1])
            opnode.left = node
        # if current token is an integer, make it the right sub tree of the
        # previous node (op node)
        if token[0] == 'int':
            opnode.right = IntNode(token[1])
            node = opnode

    return node

# Calculate the value of the expression tree using recursion


def calculate(opnode):
    # if the left sub tree is a tree, calculate its value
    if isinstance(opnode.left, OpNode):
        leftval = calculate(opnode.left)
    else:
        leftval = opnode.left.value
    if opnode.kind == '-':
        return leftval - opnode.right.value
    elif opnode.kind == '+':
        return leftval + opnode.right.value
    else:
        raise ValueError("Wrong operator")

# Determine if there is only one integer
def evaluate(node):
    # if so, return that integer
    if isinstance(node, IntNode):
        return node.value
    else:
        return calculate(node)

# main program
if __name__ == '__main__':
    # acquire string
    input = input('Input:')
    # generate token list
    tokens = getToken(input)
    # generate expression tree
    node = parse(tokens)
    # calculate result
    print("Result:" + str(evaluate(node)))
