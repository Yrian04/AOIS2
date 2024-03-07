class Node:
    def __init__(self):
        self.right = None
        self.left = None
        self.value: str | None = None

    def to_infix_form(self):
        if self.value.isalpha():
            return self.value
        left = self.left.to_infix_form() if self.left else ''
        right = self.right.to_infix_form() if self.right else ''
        return f"({left}{self.value}{right})"

    def to_prefix_form(self):
        left = self.left.to_prefix_form() if self.left else ''
        right = self.right.to_prefix_form() if self.right else ''
        return f"{self.value}{left}{right}"

    def to_postfix_form(self):
        left = self.left.to_postfix_form() if self.left else ''
        right = self.right.to_postfix_form() if self.right else ''
        return f"{left}{right}{self.value}"

    def __str__(self):
        return self.value


class LogicalFormula:
    ops = {
        '&': lambda a, b: a and b,
        '|': lambda a, b: a or b,
        '>': lambda a, b: a <= b,
        '~': lambda a, b: a == b,
        '!': lambda a, b: not b
    }

    def __init__(self):
        self.root: Node | None = None

    def build(self, expression: str):
        stack = []
        self.root = Node()
        current = self.root
        stack.append(self.root)
        processed_args = {}
        brackets = 0
        for c in expression:
            if c == '(':
                brackets += 1
                current.left = Node()
                stack.append(current)
                current = current.left
            elif c == '!':
                current = stack.pop()
                current.left = None
                current.value = c
                current.right = Node()
                stack.append(current)
                current = current.right
            elif c in self.ops:
                current.value = c
                current.right = Node()
                stack.append(current)
                current = current.right
            elif c.isalpha():
                if c not in processed_args:
                    current.value = c
                    processed_args[c] = current
                    try:
                        current = stack.pop()
                    except IndexError as e:
                        raise ValueError("Invalid expression: invalid brackets")
                else:
                    old = current
                    try:
                        current = stack.pop()
                    except IndexError as e:
                        raise ValueError("Invalid expression: invalid brackets")
                    if current.left == old:
                        current.left = processed_args[c]
                    else:
                        current.right = processed_args[c]
            elif c == ')':
                brackets -= 1
                try:
                    current = stack.pop()
                except IndexError as e:
                    raise ValueError("Invalid expression: invalid brackets")
            else:
                raise ValueError(f"Invalid expression: unknown char {c}")
        if brackets != 0:
            raise ValueError("Invalid expression: invalid brackets")

    def get_arguments(self):
        result = []

        def f(root: Node):
            if root is None:
                return
            if root.value is not None and root.value.isalpha():
                if root not in result:
                    result.append(root)
            else:
                f(root.left)
                f(root.right)

        f(self.root)
        return result

    @staticmethod
    def __process_argument(arg, length: int, level: int):
        values = []
        flag = False
        for i in range(length):
            values.append(flag)
            if (i+1) % (length // pow(2, level)) == 0:
                flag = not flag
        return {arg: values}

    def __get_start_table(self):
        result: dict[Node: list[bool]] = {}
        args = self.get_arguments()
        level = 1
        for a in args:
            result.update(self.__process_argument(a, pow(2, len(args)), level))
            level += 1
        return result

    def truth_table(self):
        result = self.__get_start_table()

        def process_operator(root: Node, table, length):
            if root is None:
                return

            left = [False]*length
            right = [False]*length
            operand1 = root.left
            if operand1 is not None:
                if operand1 not in table:
                    process_operator(operand1, table, length)
                left = table[operand1]

            operand2 = root.right
            if operand2 is not None:
                if operand2 not in table:
                    process_operator(operand2, table, length)
                right = table[operand2]

            column = [self.ops[root.value](left[i], right[i]) for i in range(length)]
            table[root] = column

        process_operator(self.root, result, pow(2, len(self.get_arguments())))
        return result

    def __list_of_answers(self) -> list[bool]:
        return self.truth_table()[self.root]

    def full_conjunctive_normal_numeric_form(self):
        result = []
        answers = self.__list_of_answers()
        if all(answers):
            return None

        for i in range(pow(2, len(self.get_arguments()))):
            if not answers[i]:
                result.append(i)

        return result

    def full_disjunctive_normal_numeric_form(self):
        result = []
        answers = self.__list_of_answers()
        if not any(answers):
            return None

        for i in range(pow(2, len(self.get_arguments()))):
            if answers[i]:
                result.append(i)

        return result

    def index_form(self):
        result = 0
        bits = self.__list_of_answers()[::-1]
        for i in range(len(bits)):
            if bits[i]:
                result += pow(2, i)
        return result

    def __to_binary(self, number):
        bits = [False]*len(self.get_arguments())
        i = len(bits) - 1
        while number > 1:
            bits[i] = number % 2 == 1
            number //= 2
            i -= 1
        bits[i] = number == 1
        return bits

    def full_conjunctive_normal_form(self):
        numeric_form = self.full_conjunctive_normal_numeric_form()
        if not numeric_form:
            return None

        args = self.get_arguments()
        result = []
        for n in numeric_form:
            bits = self.__to_binary(n)
            conj_args = []
            for i in range(len(args)):
                if bits[i]:
                    conj_args.append(f"!{args[i]}")
                else:
                    conj_args.append(f"{args[i]}")
            result.append(f"({'|'.join(conj_args)})")
        return '&'.join(result)

    def full_disjunctive_normal_form(self):
        numeric_form = self.full_disjunctive_normal_numeric_form()
        if not numeric_form:
            return None

        args = self.get_arguments()
        result = []
        for n in numeric_form:
            bits = self.__to_binary(n)
            conj_args = []
            for i in range(len(args)):
                if bits[i]:
                    conj_args.append(f"{args[i]}")
                else:
                    conj_args.append(f"!{args[i]}")
            result.append(f"({'&'.join(conj_args)})")
        return '|'.join(result)

    def __str__(self):
        return self.root.to_infix_form()
