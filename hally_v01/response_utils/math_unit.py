import random
import re
import math

from stock_responses import fail_start

math_fail = [
    "there must be something wrong with my circuitry, I failed to complete you calculation.",
    "I was unable to complete your maths question.",
    "my math's unit malfunctioned on your request",
    "did you want me to complete a maths problem?",
    "I could not compute those numbers properly",
    "in this case, I didn't know what to do with that number",
    "yes that is a number"
]

class Math_Unit(object):

    def __init__(self):
        super(Math_Unit, self).__init__()



    # this is stupid
    def simple_calc(self, sentence):

        numbers = re.findall(r'(-*[0-9]+\.*[0-9]*)+', sentence)

        ops = [
            "plus", "add", "divide", 
            "division", "over", 
            "times", "sum", "minus",
            "product", "multiply",
            "squared", "cubed", "subtract", 
            "pi", "PI", "square root", "cube root", "cubed Root", 
            "million", "thousand", "billion", "hundred",
            "to the power of"
        ]

        combined_ops = "|".join(ops)

        reg_ops = r'(?!\-[0-9])(\/|\*\*|\*|\+|\-|' + combined_ops + r')'

        operators = re.findall(reg_ops, sentence)

        if len(numbers) > 0:
            result = float(numbers[0])
            numbers.pop(0)
        else:
            return False

        numbers = map(float, numbers)

        print operators
        try: # not to be ridiculous
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
                            return "Division by zero is always undefined to me"

                    elif op == "to the power of" or op == "**":
                        result = result ** numbers[0]
                        numbers.pop(0)

                    elif op == "hundred": 
                        result = result*(10**2)
                    elif op == "thousand":
                        result = result*(10**3)
                    elif op == "million":
                        result = result*(10**6)
                    elif op == "billion":
                        result = result*(10**9)

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

                    elif op == "hundred":
                        result = result*(10**2)
                    elif op == "thousand":
                        result = result*(10**3)
                    elif op == "million":
                        result = result*(10**6)
                    elif op == "billion":
                        result = result*(10**9)


            if int(result) == float(result):
                result = int(result)
            else:
                result = round(result, 3)

            if len(operators) < 1:
                return False

            return result
        except:
            return False





    def speak_response(self, number):

        responses = [
            "my best guess is it's {0}",
            "the answer to that is {0}",
            "{0}", "{0}", "{0}", "{0}", 
            "I am pretty sure that is {0}",
            "I would say it's {0} but maybe I could be wrong",
            "my calculations suggest it is {0}"
        ]

        response = random.choice(responses)

        return response.format(number)





    def response(self, sentence, subjects):

        calculation = self.simple_calc(sentence)

        if calculation:
            if calculation == "Division by zero is always undefined to me":
                return calculation
            else:
                return self.speak_response(calculation)
        else:
            return "{0} {1}".format(random.choice(fail_start), random.choice(math_fail))

