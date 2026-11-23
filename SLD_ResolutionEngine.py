import re

class Term:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args if args else []

    def is_variable(self):
        return self.name[0].isupper()

    def __repr__(self):
        if not self.args:
            return self.name
        return f"{self.name}({', '.join(map(str, self.args))})"

class Clause:
    def __init__(self, head, body=None):
        self.head = head
        self.body = body if body else []

    def __repr__(self):
        if not self.body:
            return f"{self.head}."
        return f"{self.head} :- {', '.join(map(str, self.body))}."

# --- Unification Algorithm ---
def unify(x, y, subst):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, Term) and x.is_variable():
        return unify_variable(x, y, subst)
    elif isinstance(y, Term) and y.is_variable():
        return unify_variable(y, x, subst)
    elif isinstance(x, Term) and isinstance(y, Term):
        if x.name != y.name or len(x.args) != len(y.args):
            return None
        for ax, ay in zip(x.args, y.args):
            subst = unify(ax, ay, subst)
        return subst
    return None

def unify_variable(v, x, subst):
    if v.name in subst:
        return unify(subst[v.name], x, subst)
    if isinstance(x, Term) and x.name in subst:
        return unify(v, subst[x.name], subst)
    if occur_check(v, x, subst):
        return None
    new_subst = subst.copy()
    new_subst[v.name] = x
    return new_subst

def occur_check(v, x, subst):
    if v == x:
        return True
    elif isinstance(x, Term) and x.is_variable() and x.name in subst:
        return occur_check(v, subst[x.name], subst)
    elif isinstance(x, Term):
        return any(occur_check(v, arg, subst) for arg in x.args)
    return False

# --- Substitution Application ---
def substitute(term, subst):
    if isinstance(term, Term):
        if term.is_variable() and term.name in subst:
            return substitute(subst[term.name], subst)
        return Term(term.name, [substitute(arg, subst) for arg in term.args])
    return term

# --- Variable Standardizing (Renaming to avoid collisions) ---
var_counter = 0
def standardize_variables(clause):
    global var_counter
    var_counter += 1
    mapping = {}
    
    def rename(t):
        if t.is_variable():
            if t.name not in mapping:
                mapping[t.name] = f"{t.name}_{var_counter}"
            return Term(mapping[t.name])
        return Term(t.name, [rename(arg) for arg in t.args])
    
    new_head = rename(clause.head)
    new_body = [rename(b) for b in clause.body]
    return Clause(new_head, new_body)

# --- SLD Resolution Deduction Engine ---
def resolve(knowledge_base, goals, subst):
    if not goals:
        yield subst
        return

    current_goal = goals[0]
    remaining_goals = goals[1:]
    resolved_goal = substitute(current_goal, subst)

    for rule in knowledge_base:
        fresh_rule = standardize_variables(rule)
        next_subst = unify(resolved_goal, fresh_rule.head, subst)
        
        if next_subst is not None:
            # SLD Push: Replace current goal with the rule body
            new_goals = fresh_rule.body + remaining_goals
            yield from resolve(knowledge_base, new_goals, next_subst)

def parse_atom(string):
    match = re.match(r"(\w+)\((.+)\)", string)
    if not match: 
        return Term(string)
    name = match.group(1)
    args = [Term(arg.strip()) for arg in match.group(2).split(',')]
    return Term(name, args)
