import math
import sys

results = [] # Results list
lastResult = float(0) # Last Result
result = float(0) # Current Result

#Prints the Menu
def printMenu():
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

#Gets Input
def getInput():
    print("")
    x = int(input("Enter Menu Selection: "))
    if(x > 0 and x < 7):
        a = input("Enter first operand: ")
        b = input("Enter second operand: ")
        if(a == 'RESULT'):
            a = float(lastResult)
        if(b == 'RESULT'):
            b = float(lastResult)
        a = float(a)
        b = float(b)    
    else:
        a = 0
        b = 0
    return x, a, b

# 0: Exit
def exit(a, b):
    print("")
    print("Thanks for using this calculator. Goodbye!")
    sys.exit()

# 1: Add
def add(a, b):
    return a + b

# 2: Subtract
def sub(a, b):
    return a - b

# 3: Multiply
def mult(a, b):
    return a * b

# 4: Divide
def div(a, b):
    return a / b

# 5: Exponent
def exp(a, b):
    return a ** b

# 6: Logarithm
def log(a, b):
    return math.log(b,a)

# 7: Average
def avg(a,b):

    if(len(results) == 0):
        print("")
        print("Error: no calculations yet to average!")
    else:
        sum = 0

        for num in results:
            sum = sum + num

        numCalc = len(results)
        avg = sum / numCalc

        return sum, numCalc, round(avg, 2)

#Invalid Input
def invalidInput(a,b):
    print("")
    print("Error: Invalid selection!")

#Switch dictionary
switch = {
    0: exit,
    1: add,
    2: sub,
    3: mult,
    4: div,
    5: exp,
    6: log,
    7: avg
}

#Initial start of program
x = 0

print("Current Result: " + str(result))
print("")

printMenu()

#Program Loop
while(True):
    if(x > 0 and x < 7): printMenu()
    x, a, b = getInput()
    func = switch.get(x, invalidInput)
    result = func(a, b)
    if(x > 0 and x < 7):
        results.append(result)
        lastResult = result
        print("")
        print("Current Result: " + str(result))
        print("")
    else:
        if result is not None:
            print("")
            print("Sum of calculations: " + str(result[0]))
            print("Number of calculations: " + str(result[1]))
            print("Average of calculations: " + str(result[2]))

