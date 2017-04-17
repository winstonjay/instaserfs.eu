import re
import math

def Simple_Math(sentence):

    numbers = re.findall(r'(-*[0-9]+\.*[0-9]*)+', sentence)

    ops = [
        "plus", "add", "divide", 
        "division", "over", 
        "times", "sum", "minus",
        "product", "multiply",
        "squared", "cubed", "subtract", 
        "pi", "PI", "square root", "cube root", "cubed Root"
    ]

    combined_ops = "|".join(ops)

    reg_ops = r'(?!\-[0-9])(\/|\*|\+|\-|' + combined_ops + r')'

    operators = re.findall(reg_ops, sentence)

    if len(numbers) > 0:
        result = float(numbers[0])
        numbers.pop(0)
    else:
        return False

    numbers = map(float, numbers)

    try:
        for op in operators:
            if len(numbers) > 0:
                if op == "+" or op == "plus" or op == "add":
                    result = result + numbers[0]
                    numbers.pop(0)
                elif op == "-" or op == "minus" or op == "subtract":
                    result = result - numbers[0]
                    numbers.pop(0)
                elif op == "*" or op == "times" or op == "multiply":
                    result = result * numbers[0]
                    numbers.pop(0)
                elif op == "/" or op == "over" or op == "divide" or op == "division":
                    try:
                        result = result / numbers[0]
                        numbers.pop(0)
                    except ZeroDivisionError:
                        return "Division by zero is undefined"
                elif op == "squared":
                    result = result ** 2
                elif op == "cubed":
                    result = result ** 3
                elif op == "square root":
                    result = result ** (float(1)/2)
                elif op == "cube root" or op == "cubed root":
                    result = result ** (float(1)/3)
            else:
                if op == "squared":
                    result = result ** 2
                elif op == "cubed":
                    result = result ** 3
                elif op == "square root":
                    result = result ** (float(1)/2)
                elif op == "cube root" or op == "cubed root":
                    result = result ** (float(1)/3)

        if int(result) == float(result):
            result = int(result)
        else:
            result = round(result, 3)

        if len(operators) < 1:
            return False

        return result
    except:
        return False