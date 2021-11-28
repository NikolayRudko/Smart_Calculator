import string
from collections import deque


class Calculator:
    def __init__(self):
        self.variables = dict()
        self.go = True

    def start(self) -> None:
        """
        The method handles user input

        :return: None
        """
        operators = {'*', '/', '+', '-', '^'}
        while self.go:
            command = input().strip()
            if not command:
                continue
            # if user entered the command
            if command.startswith("/"):
                self.parser_command(command)
                continue
            # if user entered the assignment
            if '=' in command:
                self.assignment(command)
                continue
            # if user entered the calculation
            if any([o in command for o in operators]):
                self.calculate(command)
                continue
            # if user entered the output of variable
            self.print_var(command)

    def calculate(self, expression: str) -> None:
        """
        Tne method calculate expressions and print result

        :param expression: is variables with operators
        :return: None
        """
        try:
            # check for invalid operators
            if '**' in expression or '^^' in expression or '//' in expression:
                raise ValueError
            # check for count of braces
            if expression.count("(") != expression.count(")"):
                raise ValueError
            # replace variables with values
            for key, value in self.variables.items():
                if key in expression:
                    expression = expression.replace(key, value)
            # check unknown variables
            if any([letter in expression for letter in string.ascii_letters]):
                raise ValueError
            members = self.to_sequence(expression)
            result = self.calculate_expression(members)
            if result % 1 == 0:
                result = int(result)
            print(result)
        except ValueError:
            print("Invalid expression")

    def to_sequence(self, expression: str) -> list:
        """
        Convert expression to sequence of members.

        :param expression:
        :return: sequence of members
        """
        support_operators = {'+', '-', '*', '/', '^', "(", ')'}
        parasite_operators = {"++", "--", '+-', '-+'}
        expression = expression.replace(" ", "")
        while any([i in expression for i in parasite_operators]):
            expression = expression.replace("--", "+").replace('+-', '-').replace('-+', '-').replace('++', '+')
        for operator in support_operators:
            expression = expression.replace(operator, f" {operator} ")
        return expression.split()

    def calculate_expression(self, expression: list) -> float:
        """
        Calculate expression

        :param expression:
        :return: result of expression
        """
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, "(": 0, ')': 0}
        digit_stack = deque()
        operand_stack = deque()
        for mem in expression:
            if mem.isdigit():
                digit_stack.append(int(mem))
            else:
                if mem == "(":
                    operand_stack.append(mem)
                elif operand_stack and priority[mem] > priority[operand_stack[-1]]:
                    operand_stack.append(mem)
                elif operand_stack and priority[mem] <= priority[operand_stack[-1]]:
                    while operand_stack and priority[mem] <= priority[operand_stack[-1]] \
                            and priority[operand_stack[-1]] > 0:
                        y = digit_stack.pop()
                        x = digit_stack.pop()
                        operand = operand_stack.pop()
                        z = self.do_operation(x, y, operand)
                        digit_stack.append(z)

                    if priority[mem] == 0 and priority[operand_stack[-1]] == 0:
                        operand_stack.pop()
                    else:
                        operand_stack.append(mem)
                else:
                    operand_stack.append(mem)

        while operand_stack:
            y = digit_stack.pop()
            x = digit_stack.pop()
            operand = operand_stack.pop()
            z = self.do_operation(x, y, operand)
            digit_stack.append(z)

        if len(digit_stack) != 1:
            raise ValueError
        else:
            return digit_stack.pop()

    def do_operation(self, x: float, y: float, operator: str) -> float:
        """
        Does basic mathematical operations

        :param x: first operand
        :param y: second operand
        :param operator: type of operation
        :return: result of operation
        """
        if operator == '-':
            return x - y
        if operator == '+':
            return x + y
        if operator == '*':
            return x * y
        if operator == "/":
            return x / y
        if operator == "^":
            return x ** y

    def assignment(self, expression: str) -> None:
        """
        Assign a value to a variable

        :param expression: user command
        :return: None
        """
        try:
            var_l, var_r = [var.strip() for var in expression.split('=')]
            if not var_l.isalpha():
                raise TypeError
            elif var_l.isdigit() or (var_r not in self.variables and not var_r.isdigit()):
                raise ValueError
            elif var_r.isdigit():
                self.variables[var_l] = var_r
            else:
                self.variables[var_l] = self.variables[var_r]
        except ValueError:
            print('Invalid assignment')
        except TypeError:
            print("Invalid identifier")

    def print_var(self, var: str) -> None:
        print(self.variables[var] if var in self.variables else 'Unknown variable')

    def parser_command(self, command: str) -> None:
        """
        Handles user commands

        :param command: User command
        :return: None
        """
        if command == "/exit":
            print("Bye!")
            self.go = False
        elif command == "/help":
            print("The program do some mathematical operations according to the input operator:\n" +
                  "Create variables;\n" +
                  "Print value of variables\n" +
                  "Adding numbers and variables;\n" +
                  "Subtraction of numbers and variables;\n" +
                  "Multiplication of numbers and variables;\n" +
                  "Division of numbers and variables;\n" +
                  "Power of numbers and variables;\n" +
                  "Support of braces.")
        else:
            print('Unknown command')


def main() -> None:
    smart_calculator = Calculator()
    smart_calculator.start()


if __name__ == "__main__":
    main()
