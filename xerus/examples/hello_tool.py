"""
Example tool for Xerus CLI.
This file demonstrates how to create a custom tool for the Xerus CLI.
"""
from smolagents import Tool

class HelloTool(Tool):
    name = "hello_tool"
    description = """
    A simple tool that greets the user with a customized message.
    It returns a greeting message with the given name and language.
    """
    
    inputs = {
        "name": {
            "type": "string",
            "description": "The name to include in the greeting.",
        },
        "language": {
            "type": "string",
            "description": "The language for the greeting (e.g., 'english', 'spanish', 'french').",
        }
    }
    
    output_type = "string"
    
    def forward(self, name: str, language: str = "english"):
        """
        Generate a greeting in the specified language.
        
        Args:
            name: The name to include in the greeting
            language: The language for the greeting
            
        Returns:
            A greeting message
        """
        greetings = {
            "english": f"Hello, {name}! How are you today?",
            "spanish": f"¡Hola, {name}! ¿Cómo estás hoy?",
            "french": f"Bonjour, {name}! Comment vas-tu aujourd'hui?",
            "german": f"Hallo, {name}! Wie geht es dir heute?",
            "italian": f"Ciao, {name}! Come stai oggi?",
            "japanese": f"こんにちは、{name}さん！今日の調子はどうですか？",
        }
        
        # Default to English if language not supported
        return greetings.get(language.lower(), f"Hello, {name}! How are you today?")

# Create an instance of the tool so it can be imported directly
hello_tool = HelloTool()

# You can test the tool directly
if __name__ == "__main__":
    result = hello_tool(name="World", language="english")
    print(result)  # Output: Hello, World! How are you today? 