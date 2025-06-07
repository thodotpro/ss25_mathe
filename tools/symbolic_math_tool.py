import sympy as sp

class SymbolicMathTool:
    name = "symbolic_math"
    description = "Performs symbolic mathematics operations using SymPy. Example: 'integrate x^2 dx' returns the integral of x^2. Now supports multiple variables (e.g., x, y, z)."

    @staticmethod
    def run(params: dict):
        expression = params.get("expression")
        if not expression:
            return "Error: No expression provided."

        # Get variables (default to ['x'] if not provided)
        variables = params.get("variables", ["x"])
        if not isinstance(variables, list):
            variables = [variables]
        try:
            syms = sp.symbols(variables)
        except Exception as e:
            return f"Error: Invalid variable(s): {variables}. {e}"

        # Parse the expression
        try:
            parsed_expr = sp.sympify(expression, locals={v: s for v, s in zip(variables, syms)})
        except Exception as e:
            return f"Error: Could not parse expression. {e}"

        op = params.get("operation")
        if op == "integrate":
            # Integrate with respect to all variables in order
            try:
                result = parsed_expr
                for sym in syms:
                    result = sp.integrate(result, sym)
            except Exception as e:
                return f"Error: Integration failed. {e}"
        elif op == "differentiate":
            # Differentiate with respect to all variables in order
            try:
                result = parsed_expr
                for sym in syms:
                    result = sp.diff(result, sym)
            except Exception as e:
                return f"Error: Differentiation failed. {e}"
        else:
            return "Error: Unsupported operation."

        return str(result)