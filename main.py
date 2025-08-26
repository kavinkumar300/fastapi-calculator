from fastapi import FastAPI, Query, HTTPException
from enum import Enum
from typing import Optional
import math

app = FastAPI(title="Simple Calculator using FastAPI with history")

class Operation(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"
    power = "power"
    modulus = "modulus"
    sqrt = "sqrt"      
    factorial = "factorial"  
    log = "log"              
    log10 = "log10"          


history = []

def add_to_history(entry: str):
    if len(history) >= 10:
        history.pop(0)
    history.append(entry)

@app.post("/calculate/")
def calculate(
    operation: Operation,
    a: float = Query(..., description="First number"),
    b: Optional[float] = Query(None, description="Second number (optional for some operations)")
):
    try:
        
        if operation == Operation.add:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for addition")
            result = a + b
            add_to_history(f"ADD: {a} + {b} = {result}")

        elif operation == Operation.subtract:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for subtraction")
            result = a - b
            add_to_history(f"SUBTRACT: {a} - {b} = {result}")

        elif operation == Operation.multiply:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for multiplication")
            result = a * b
            add_to_history(f"MULTIPLY: {a} × {b} = {result}")

        elif operation == Operation.divide:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for division")
            if b == 0:
                raise HTTPException(status_code=400, detail="Division by zero is not allowed")
            result = a / b
            add_to_history(f"DIVIDE: {a} ÷ {b} = {result}")

        elif operation == Operation.power:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for power")
            result = math.pow(a, b)
            add_to_history(f"POWER: {a}^{b} = {result}")

        elif operation == Operation.modulus:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for modulus")
            result = a % b
            add_to_history(f"MODULUS: {a} % {b} = {result}")

        elif operation == Operation.sqrt:
            if b is None:
                raise HTTPException(status_code=400, detail="Second number is required for sqrt operation")
            if b < 0:
                raise HTTPException(status_code=400, detail="Square root of negative numbers is not allowed")
            result = math.sqrt(b)
            add_to_history(f"SQRT: √{b} = {result}")

       
        elif operation == Operation.factorial:
            if a < 0:
                raise HTTPException(status_code=400, detail="Factorial of negative numbers is not allowed")
            if not float(a).is_integer():
                raise HTTPException(status_code=400, detail="Factorial is only defined for integers")
            result = math.factorial(int(a))
            add_to_history(f"FACTORIAL: {a}! = {result}")

        elif operation == Operation.log:
            if a <= 0:
                raise HTTPException(status_code=400, detail="Logarithm is only defined for positive numbers")
            if b and b > 0 and b != 1:
                result = math.log(a, b)
                add_to_history(f"LOG: log base {b} of {a} = {result}")
            else:
                result = math.log(a)
                add_to_history(f"LOG: ln({a}) = {result}")

        elif operation == Operation.log10:
            if a <= 0:
                raise HTTPException(status_code=400, detail="Log10 is only defined for positive numbers")
            result = math.log10(a)
            add_to_history(f"LOG10: log10({a}) = {result}")

        else:
            raise HTTPException(status_code=400, detail="Invalid operation")

        return {"operation": operation, "a": a, "b": b, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/")
def get_history():
    return {"last_10_calculations": history}
