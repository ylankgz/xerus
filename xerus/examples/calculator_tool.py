"""
Example calculator tool for Xerus CLI.
This file demonstrates how to create a more complex custom tool for the Xerus CLI.
"""
from typing import Union, Dict, Any
from smolagents import Tool

class CalculatorTool(Tool):
    name = "calculator"
    description = """
    A calculator tool that performs basic arithmetic operations.
    It supports addition, subtraction, multiplication, division, and exponentiation.
    """
    
    inputs = {
        "operation": {
            "type": "string",
            "description": "The operation to perform (add, subtract, multiply, divide, power).",
            "enum": ["add", "subtract", "multiply", "divide", "power"]
        },
        "a": {
            "type": "number",
            "description": "The first operand.",
        },
        "b": {
            "type": "number",
            "description": "The second operand.",
        }
    }
    
    output_type = "object"
    
    def forward(self, operation: str, a: float, b: float) -> Dict[str, Any]:
        """
        Perform the specified arithmetic operation.
        
        Args:
            operation: The operation to perform
            a: The first operand
            b: The second operand
            
        Returns:
            A dictionary containing the result and a description
        """
        result = None
        description = ""
        
        if operation == "add":
            result = a + b
            description = f"The sum of {a} and {b}"
        elif operation == "subtract":
            result = a - b
            description = f"The difference of {a} and {b}"
        elif operation == "multiply":
            result = a * b
            description = f"The product of {a} and {b}"
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            result = a / b
            description = f"The quotient of {a} divided by {b}"
        elif operation == "power":
            result = a ** b
            description = f"{a} raised to the power of {b}"
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return {
            "result": result,
            "description": description,
            "operation": operation,
            "a": a,
            "b": b
        }

# Create an instance of the tool so it can be imported directly
calculator_tool = CalculatorTool()

# You can test the tool directly
if __name__ == "__main__":
    result = calculator_tool(operation="add", a=5, b=3)
    print(f"Result: {result['result']}")  # Output: Result: 8
    print(f"Description: {result['description']}")  # Output: Description: The sum of 5 and 3
    
    # Test other operations
    print(calculator_tool(operation="subtract", a=10, b=4))
    print(calculator_tool(operation="multiply", a=6, b=7))
    print(calculator_tool(operation="divide", a=9, b=3))
    print(calculator_tool(operation="power", a=2, b=3)) 