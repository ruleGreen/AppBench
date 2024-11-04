import math

# Define a Calculator class
class Calculator:
    def __init__(self):
        self.desc = {
            "desc": "a simple calculator app",
            "base_required_arguments": {
                "None": "No required arguments"
            },
            "APIs": {
                "calculate_from_string": {
                    "args": {
                        "expression": "str"
                    },
                    "returns": "float or str"
                }
              
            }
        }

    # Method to perform calculations from string input
    def calculate_from_string(self, expression):
        """
        Perform calculation from a string expression

        Parameters:
            expression (str): The arithmetic expression as a string

        Returns:
            float or str: The result of the calculation or an error message
        """
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {str(e)}"


# Example usage
def main():
    # Create a calculator object
    calc = Calculator()

    print("Welcome to the calculator!")
    
    # Get the expression from the user
    expression = input("Enter the arithmetic expression (e.g., 2+3-9): ")

    # Call the calculate_from_string method to perform the calculation
    result = calc.calculate_from_string(expression)
    
    # Print the result
    print(f"The result is: {result}")
    

# Call the main function
if __name__ == "__main__":
    main()