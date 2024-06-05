def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 == 0:
            return "Error: Division by zero is undefined."
        else:
            return num1 / num2
    else:
        return "Invalid operation."

def main():
    print("Welcome to Simple Calculator")
    
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    print("Choose an operation: +, -, *, /")
    
    while True:
        operation = input("Enter your choice: ")
        if operation in ['+', '-', '*', '/']:
            break
        else:
            print("Invalid operation. Please choose from +, -, *, /")

    result = calculate(num1, num2, operation)

    print(f"The result is: {result}")

if __name__ == "__main__":
    main()
