import math

class Calculator:
    def __init__(self, mode="deg"):
        self.mode = mode

        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3,
            "fact": 4.
        }
        self.right_associative = {"^"}
        
        def safe_root(x,n):
            if n<0 and x%2 == 0:
                raise ValueError("Cannot take an even root of a negative number")
            return n ** (1/x)

        self.functions = {
            "root": safe_root,
            "sqrt": math.sqrt,
            "cbrt": lambda x: x ** (1/3),
            "log": math.log10,
            "ln": math.log,
            "inv": lambda x: 1 / x,
            "sin": lambda x: math.sin(self._angle_mode(x)),
            "cos": lambda x: math.cos(self._angle_mode(x)),
            "tan": lambda x: math.tan(self._angle_mode(x)),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "deg": math.degrees,
            "rad": math.radians,
            "fact": lambda x: math.factorial(int(x)),
            "neg": lambda x: -x,
        }

        self.constants = {
            "pi": math.pi,
            "e": math.e,
        }

    def _angle_mode(self, x):
        return math.radians(x) if self.mode == "deg" else x

    def set_mode(self, mode="deg"):
        self.mode = mode

    def toggle_mode(self):
        self.mode = "rad" if self.mode == "deg" else "deg"

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        try:
            tokens = self._tokenize(expression)
            return self._evaluate_infix(tokens)
        except Exception as e:
            raise ValueError(f"invalid expression: {e}") from e

    def _tokenize(self, expression):
        tokens, num, func, prev = [], "", "", None
        expr = expression.replace(" ", "")
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch.isdigit() or ch == ".":
                num += ch
                prev = "num"
            elif ch.isalpha():
                if prev == "num" or prev == "paren_close":
                    tokens.append("*")
                func += ch
                prev = "func"
            else:
                if num:
                    tokens.append(num)
                    num = ""
                if func:
                    tokens.append(func)
                    func = ""
                if ch in "+-":
                    if prev is None or prev in ("op", "paren_open"):
                        if ch == "-":
                            tokens.append("neg")
                        i += 1
                        continue
                if ch in self.operators:
                    tokens.append(ch)
                    prev = "op"
                elif ch == "(":
                    if prev in ("num", "paren_close", "const"):
                        tokens.append("*")
                    tokens.append(ch)
                    prev = "paren_open"
                elif ch == ")":
                    tokens.append(ch)
                    prev = "paren_close"
                elif ch == ",":
                    tokens.append(ch)
                    prev = "op"
                elif ch == "!":
                    tokens.append("fact")
                    prev = "func"
                else:
                    raise ValueError(f"Invalid character: {ch}")
            i += 1
        if num:
            tokens.append(num)
        if func:
            tokens.append(func)
        return tokens

    def _evaluate_infix(self, tokens):
        values, operators = [], []
        op_and_fact = set(self.operators.keys()) | {"fact"}
        
        for token in tokens:
            if token in op_and_fact:
                while (
                    operators
                    and operators[-1] in op_and_fact
                    and (
                        self.precedence[operators[-1]] > self.precedence[token]
                        or (
                            self.precedence[operators[-1]] == self.precedence[token]
                            and token not in self.right_associative
                        )
                    )
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            elif token in self.functions:
                operators.append(token)
                
            elif token in self.constants:
                values.append(self.constants[token])
                
            elif token == "(":
                operators.append(token)
                
            elif token == ",":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != '(':
                    raise ValueError("Comma found outside of function arguments")

            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != "(":
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Pop the opening '('
                if operators and operators[-1] in self.functions and operators[-1] != "fact":
                    self._apply_operator(operators, values)
            else:
                values.append(float(token))

        while operators:
            if operators[-1] == "(":
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)
        if len(values) != 1:
            raise ValueError("Invalid expression")
        return values[0]

    def _apply_operator(self, operators, values):
        op = operators.pop() 
        if op in self.functions:
            if op == 'root':
                if len(values) < 2: raise ValueError("Not enough arguments for root")
                # The arguments are popped in reverse order (n, then x)
                n, x = values.pop(), values.pop()
                values.append(self.functions[op](x, n))
            else:  # All other functions (sin, log, fact, etc.) are unary
                if len(values) < 1: raise ValueError(f"Not enough arguments for {op}")
                val = values.pop()
                values.append(self.functions[op](val))
        else:  # It's a binary operator like +, -, *
            if len(values) < 2: raise ValueError(f"Not enough operands for operator: {op}")
            b, a = values.pop(), values.pop()
            values.append(self.operators[op](a, b))