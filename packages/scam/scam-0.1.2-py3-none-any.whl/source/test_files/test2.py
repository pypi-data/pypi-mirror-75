#this is exercise 1 taken from this class, the scientific calculator
import math
result = 0.0
sum = 0.0
calcs = 0
average = 0.0
calculatorrunning = True
def main():
    while (calculatorrunning):
        handleInput(Menu())
    print("")
    print("Thanks for using this calculator. Goodbye!")
def Menu():
    global result
    """if (result == "UNDEFINED"):
        print("Current Result: UNDEFINED (result is set to 0)", result)
        result = 0.0
    else:"""
    print("Current Result:", result)
    print("")
    print("Calculator Menu")
    print("---------------")
    print("0. Exit Program")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exponentiation")
    print("6. Logarithm")
    print("7. Display Average")
    print("")
    menuanswer = int(input('Enter Menu Selection: '))
    return menuanswer

def handleInput(menuanswer):
    global result
    global calculatorrunning
    global sum, calcs, average
    if (menuanswer == 0):
        calculatorrunning = False
        return
    elif (menuanswer >= 1 and menuanswer <= 6):
        op1, op2 = getInputs()
        if (menuanswer == 1):
            result = op1 + op2
        elif (menuanswer == 2):
            result = op1 - op2
        elif (menuanswer == 3):
            result = op1 * op2
        elif (menuanswer == 4):
            result = op1/op2
        elif (menuanswer == 5):
            result = op1**op2
        elif (menuanswer == 6):
            result = math.log(op2, op1)
    elif (menuanswer == 7):
        print("")
        if (calcs == 0):
            print("Error: No calculations yet to average!")
        else:
            print("Sum of calculations:", sum)
            print("Number of calculations:", calcs)
            if (isinstance(sum, complex)):
                print("Average of calculations:", sum/float(calcs))
            else:
                print("Average of calculations:", round(sum/float(calcs), 2))
        print("")
        handleInput(int(input('Enter Menu Selection: ')))
        return
        """if (op2 == 0):
                if (op1 == 0):
                    result = "UNDEFINED"
                else:
                    result = 1
            elif (op2 <= -1):
                result = 1.0/op1
                for i in range(absop2 - 1):
                    result *= op1
            elif (op2 >= 1):
                result = op1
                for i in range(op2 - 1):
                    result *= op1"""
    else:
        print("")
        print("Error: Invalid selection!")
        print("")
        handleInput(int(input('Enter Menu Selection: ')))
        return
    sum += result
    calcs += 1
    print("")

def getInputs():
    op1 = input("Enter first operand: ")
    op2 = input("Enter second operand: ")
    if (op1 == "RESULT"):
        op1 = result
    op1 = float(op1)
    if (op2 == "RESULT"):
        op2 = result
    op2 = float(op2)
    return op1, op2

main()