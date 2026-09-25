import os
import pickle

class AlgebraicLispInterpreter:
    def __init__(self):
        # 📋 State registers for your 5th-grade sensors
        self.game_sensors = {
            "velocity": 4,
            "distance_to_school": 5820
        }

    def tokenize(self, code_string):
        """Converts raw S-expressions into nested Python lists."""
        spaced = code_string.replace('(', ' ( ').replace(')', ' ) ')
        return [t for t in spaced.split() if t.strip()]

    def parse_tokens(self, tokens):
        """Recursively builds an execution-ready Abstract Syntax Tree."""
        if len(tokens) == 0:
            raise SyntaxError("Unexpected EOF while parsing algebraic matrix.")
        
        token = tokens.pop(0)
        if token == '(':
            sub_list = []
            while tokens and tokens[0] != ')':
                sub_list.append(self.parse_tokens(tokens))
            if tokens and tokens[0] == ')':
                tokens.pop(0) # Remove closing parenthetical
            return sub_list
        elif token == ')':
            raise SyntaxError("Mismatched closing bracket layout.")
        else:
            return self.atomize(token)

    def atomize(self, token):
        """Resolves raw tokens into numeric primitives or symbolic atoms."""
        try:
            if '.' in token: return float(token)
            return int(token)
        except ValueError:
            return str(token)

    def evaluate(self, exp):
        """👑 RECURSIVE ALGEBRAIC EVALUATOR: Runs operations and maintains symbols."""
        if not isinstance(exp, list):
            if exp in self.game_sensors:
                return self.game_sensors[exp]
            return exp

        if not exp:
            return None

        operator = exp[0]

        # 🧮 Algebraic and Arithmetic Operators
        if operator == '*':
            left = self.evaluate(exp[1])
            right = self.evaluate(exp[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            return f"(* {left} {right})"

        elif operator == '/':
            left = self.evaluate(exp[1])
            right = self.evaluate(exp[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left / right
            return f"(/ {left} {right})"

        elif operator == '-':
            left = self.evaluate(exp[1])
            right = self.evaluate(exp[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            return f"(- {left} {right})"

        elif operator == '+':
            left = self.evaluate(exp[1])
            right = self.evaluate(exp[2])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            return f"(+ {left} {right})"

        elif operator == '==' or operator == 'eq':
            left = self.evaluate(exp[1])
            right = self.evaluate(exp[2])
            return left == right

        # 🧭 Action Function Fallbacks
        else:
            evaluated_args = [self.evaluate(arg) for arg in exp[1:]]
            return f"({operator} " + " ".join(map(str, evaluated_args)) + ")"

    def run_algebraic_suite(self):
        print("=" * 95)
        print("🌀 LIVE LISP ALGEBRAIC INTERPRETER & 5TH GRADE TRAVEL SOLVER")
        print("=" * 95)

        # 📋 Problem: Distance = 5820 ft, Velocity = 4 ft/sec. Find time.
        travel_sketch = "(/ distance_to_school velocity)"
        
        tokens = self.tokenize(travel_sketch)
        ast = self.parse_tokens(tokens)
        total_seconds = self.evaluate(ast)
        
        # Format the raw seconds back into human-readable minutes
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        print(f"📥 Story Problem Ingested ──➔ Girl walking 5820 ft at 4 ft/sec.")
        print(f"   ├── Compiled S-Expression ──➔ {travel_sketch}")
        print(f"   ├── Evaluated Raw Output  ──➔ \033[1;32m{total_seconds} seconds\033[0m")
        print(f"   └── Human-Readable Result ──➔ \033[1;32m{minutes} minutes and {seconds} seconds\033[0m")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
    exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
    os.makedirs(os.path.dirname(exs_path), exist_ok=True)
    with open(exs_path, "w", encoding="utf-8") as f:
        f.write("synthesis_status(school_walking_story, schema_travel_closure).\n")

    engine = AlgebraicLispInterpreter()
    engine.run_algebraic_suite()
