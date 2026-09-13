# Save this file inside: backend/math_parser.py

import ast
import math
import operator

class ScientificMathParser:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    The 0th fundamental model of the application. It safely tokenizes and evaluates 
    standard arithmetic and scientific keyboard inputs from the calculator view.
    It completely avoids the unsafe 'eval()' mechanism to ensure total mobile sandbox safety.

    IN-LINE THEORY REFRESHER:
    ------------------------
    Expression parsing converts a dynamic text string into structural mathematical nodes.
    It strictly enforces operational operator hierarchies (BODMAS/PEMDAS):
    Parentheses -> Exponents -> Multiplication/Division -> Addition/Subtraction.
    """

    def __init__(self, raw_expression: str):
        """
        INITIALIZATION & STRING SANITIZATION PIPELINE
        --------------------------------------------
        Cleans up interface formatting irregularities (like spaces or special characters) 
        and prepares the mathematical expression string for safe processing.
        
        :param raw_expression: The unformatted text input string from the screen layout (e.g., "5 + 3 * 2").
        """
        if not raw_expression or not raw_expression.strip():
            raise ValueError("Input Error: The expression string cannot be empty.")
            
        # Clean white space formatting issues and align common calculator symbol variations
        self.expression = raw_expression.strip().replace("×", "*").replace("÷", "/").replace("−", "-")
        
        # Whitelist of safe structural operations allowed to execute within our compiler tree
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,  # Support for negative numbers like -5
            ast.UAdd: operator.pos   # Support for explicit positive declarations like +5
        }

    def _evaluate_node(self, node):
        """
        RECURSIVE PRIVATE COMPILER NODE PROCESSING
        ------------------------------------------
        Recursively steps through the tree nodes to solve equations safely.
        """
        # Node Type 1: Constant number values
        if isinstance(node, ast.Constant):
            return float(node.value)
            
        # Node Type 2: Standard Binary Math Operations (e.g., Left Element + Right Element)
        elif isinstance(node, ast.BinOp):
            if type(node.op) in self.allowed_operators:
                left_val = self._evaluate_node(node.left)
                right_val = self._evaluate_node(node.right)
                return self.allowed_operators[type(node.op)](left_val, right_val)
            raise TypeError(f"Execution Error: Operator '{type(node.op).__name__}' is blocked for security.")
            
        # Node Type 3: Unary Operators (e.g., prepended negative signs like -10)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) in self.allowed_operators:
                operand_val = self._evaluate_node(node.operand)
                return self.allowed_operators[type(node.op)](operand_val)
            raise TypeError(f"Execution Error: Unary '{type(node.op).__name__}' is blocked for security.")
            
        raise TypeError("Syntax Error: Unauthorized expression format detected.")

    def get_calculated_result(self) -> float:
        """
        OUTPUT OPTION A: THE COMPUTED DECIMAL ANSWER
        -------------------------------------------
        Parses the text string stringently via the Abstract Syntax Tree and processes 
        the arithmetic to return a highly precise numerical float result.
        """
        try:
            # Transform text into safe mathematical syntax tree nodes
            tree_root = ast.parse(self.expression, mode='eval')
            raw_result = self._evaluate_node(tree_root.body)
            
            # Formats to a clean integer if there are no fractional values, otherwise rounds to 6 decimals
            if raw_result.is_integer():
                return int(raw_result)
            return round(raw_result, 6)
            
        except ZeroDivisionError:
            raise ValueError("Math Error: Cannot divide by zero.")
        except Exception:
            raise ValueError("Syntax Error: Please verify that brackets and math operators are placed correctly.")

    def get_formatted_recap(self) -> str:
        """
        OUTPUT OPTION B: FORMATTED CALCULATOR DISPLAY STREAM
        ---------------------------------------------------
        Cleans up the user's raw string syntax to present a beautiful, polished 
        recap layout stream right above the primary mobile app screen answer box.
        """
        # Puts clean, standard spaces around foundational operators to look highly professional
        recap_string = self.expression
        for op in ["+", "*", "/", "^"]:
            recap_string = recap_string.replace(op, f" {op} ")
        return " ".join(recap_string.split())
