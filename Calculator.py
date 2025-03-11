# Python calculator

operation = input("Enter an operation (+ - * /): ")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

if operation == "+":
    result = num1 + num2
    print(f"The result: {round(result, 3)}")
elif operation =="-":
    result = num1 - num2
    print(f"The result: {round(result, 3)}")
elif operation == "*":
    result = num1 * num2
    print(f"The result: {round(result, 3)}")
elif operation == "/":
    if num2 == 0:
        print("The second number should be not 0");
    else:
        result = num1 / num2
        print(f"The result: {round(result, 3)}")
