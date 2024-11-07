def calculator():
    while True:
        expression = input("Enter the mathematical expression (e.g., 1+3-5*2): ")

        try:
            # Evaluate the expression using eval
            result = eval(expression)
            print(f"The result is: {result}")
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")
        except Exception as e:
            print(f"Error: Invalid input ({e})")

        if expression.lower() == 'exit':
            break

calculator()
