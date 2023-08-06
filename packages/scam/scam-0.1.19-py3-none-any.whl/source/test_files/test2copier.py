#this version is taken from a theoretical copier who may have cheated from #test2.py, it posseses slight variations
import math
res = 0
summa = 0
calcor = 0.0
average = 0
calculatorrunning = True
def main():
    while (calculatorrunning):
        handleInput(Menu())
    print("Thanks for completing my program!")
def menu():
    global result
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
            print("error: No calculations yet to average!")
        else:
            print("sum of calculations:", sum)
            print("number of calculations:", calcs)
            if (isinstance(sum, complex)):
                print("Average of calculations:", sum/float(calcs))
            else:
                print("Average of calculations:", round(sum/float(calcs), 2))
        print("")
        handleInput(int(input('Enter Menu Selection: ')))
        return
    else:
        print("")
        print("Error: Invalid selection!")
        print("")
        handleInput(int(input('Enter Menu Selection: ')))
        return
    calcor += 1
    summa += result
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