# This program adds two numbers
def sums():
    num1 = 1.5
    num2 = 6.3

    # Add two numbers
    sum1 = 0
    if num1 == 1.5:
        sum1 = num1 + num2

    for i in range(0, 10):
        num2 += i

    # Display the sum
    print('The sum of {0} and {1} is {2}'.format(num1, num2, sum1))

    num3 = 3
    num4 = 9

    # Add two numbers
    sum2 = num3 + num4

    # Display the sum
    print('The sum of {0} and {1} is {2}'.format(num3, num4, sum2))

sums()