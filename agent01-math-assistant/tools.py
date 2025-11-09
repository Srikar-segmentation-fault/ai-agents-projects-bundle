# ============================================================
# tools.py
# ============================================================
# Defines all the custom and built-in tools used by the agent.
# Includes mathematical tools, Wikipedia search, and an example
# of a structured tool using Pydantic for validated input schemas.
# ============================================================

import re
from typing import List
from pydantic import BaseModel, Field

# LangChain imports
from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools.structured import StructuredTool


# ============================================================
# 1️⃣ ADDITION TOOL — Simple Free-Text Tool
# ============================================================
@tool
def add_numbers(text: str) -> str:
    """
    Extracts all numeric values from text and returns their sum.

    Example:
        Input: "Add 12, 8 and 5"
        Output: "25"
    """
    numbers = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]
    if not numbers:
        return "No numbers found."
    return f"{sum(numbers):.4g}"


# ============================================================
# 2️⃣ SUBTRACTION TOOL
# ============================================================
@tool
def subtract_numbers(text: str) -> str:
    """
    Extracts numbers and performs sequential subtraction.
    Example:
        Input: "Subtract 10, 2, and 3"
        Output: "5"
    """
    numbers = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]
    if not numbers:
        return "No numbers found."
    result = numbers[0]
    for n in numbers[1:]:
        result -= n
    return f"{result:.4g}"


# ============================================================
# 3️⃣ MULTIPLICATION TOOL
# ============================================================
@tool
def multiply_numbers(text: str) -> str:
    """
    Multiplies all numeric values found in the text.
    Example:
        Input: "Multiply 2, 3 and 4"
        Output: "24"
    """
    numbers = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]
    if not numbers:
        return "No numbers found."
    result = 1
    for n in numbers:
        result *= n
    return f"{result:.4g}"


# ============================================================
# 4️⃣ DIVISION TOOL
# ============================================================
@tool
def divide_numbers(text: str) -> str:
    """
    Divides numbers sequentially in the order they appear.
    Example:
        Input: "Divide 100 by 5 and then by 2"
        Output: "10"
    """
    numbers = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]
    if not numbers:
        return "No numbers found."
    result = numbers[0]
    try:
        for n in numbers[1:]:
            if n == 0:
                return "Error: Division by zero."
            result /= n
        return f"{result:.4g}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================
# 5️⃣ POWER TOOL (Exercise Example)
# ============================================================
class PowerInput(BaseModel):
    """Defines the structured input schema for the power tool."""
    base: float = Field(..., description="Base number")
    exponent: float = Field(..., description="Exponent value")

def calculate_power(base: float, exponent: float) -> str:
    """Raises base to exponent and returns the result."""
    try:
        return f"{pow(base, exponent):.4g}"
    except Exception as e:
        return f"Error: {str(e)}"

power_numbers = StructuredTool.from_function(
    func=calculate_power,
    name="power_numbers",
    description="Calculates the power of a base number raised to an exponent.",
    args_schema=PowerInput
)


# ============================================================
# 6️⃣ WIKIPEDIA TOOL (Built-in)
# ============================================================
wiki_api = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api)


# ============================================================
# 7️⃣ COMBINED TOOLS LIST (Optional Helper)
# ============================================================
# Export all tools so they can be imported directly in main.py
all_tools = [
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    power_numbers,
    wiki_tool,
]

# ============================================================
# ✅ NOTES:
# - The @tool decorator creates a single-input tool (string-based).
# - StructuredTool allows multiple validated inputs (via BaseModel).
# - Wikipedia tool uses built-in community modules.
# ============================================================
