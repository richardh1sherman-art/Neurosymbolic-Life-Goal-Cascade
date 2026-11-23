
# Add 'substitute' to this import statement
from SLD_ResolutionEngine import Term, Clause, parse_atom, resolve, substitute

# Your background knowledge and execution code follows:
kb = [
    Clause(parse_atom("parent(alice, bob)")),
    Clause(parse_atom("parent(bob, charlie)")),
    Clause(parse_atom("ancestor(X, Y)"), [parse_atom("parent(X, Y)")]),
    Clause(parse_atom("ancestor(X, Y)"), [parse_atom("parent(X, Z)"), parse_atom("ancestor(Z, Y)")]),
]

query_goal = [parse_atom("ancestor(X, charlie)")]

print(f"Querying: {query_goal}")
solutions = list(resolve(kb, query_goal, {}))

for idx, sol in enumerate(solutions):
    # Unwind the substitutions by applying them back to your original query atom
    resolved_atom = substitute(query_goal[0], sol)
    
    # Extract the first argument, which corresponds to the 'X' position
    concrete_value = resolved_atom.args[0]
    
    print(f"Solution {idx + 1}: X = {concrete_value}")

