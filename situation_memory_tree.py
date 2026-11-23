import os
import math
import collections

class SituationNode:
    """An advanced Neuro-Symbolic node featuring terminal leaf modification routines."""
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, preserved_context=None):
        self.col = col                      # Split column index
        self.value = value                  # Split criteria constant
        self.results = results              # Distribution map (Leaf only)
        self.tb = tb                        # True Branch pointer
        self.fb = fb                        # False Branch pointer
        self.preserved_context = preserved_context  # Cached feature context map

def divideset(rows, column, value):
    split_function = lambda row: float(row[column]) >= float(value) if isinstance(value, (int, float)) else lambda row: str(row[column]) == str(value)
    set1 = [row for row in rows if str(row[column]) == str(value)]
    set2 = [row for row in rows if str(row[column]) != str(value)]
    return (set1, set2)

def uniquecounts(rows):
    results = {}
    for row in rows:
        r = row[-1]
        if r not in results: results[r] = 0
        results[r] += 1
    return results

def entropy(rows):
    if len(rows) == 0: return 0.0
    results = uniquecounts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * (math.log(p) / math.log(2))
    return ent

def build_situation_memory_tree(rows, scorefun=entropy):
    """👑 CONTEXT-PRESERVING LEAF NETWORK COMPILER"""
    if len(rows) == 0: return SituationNode()
    current_score = scorefun(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        column_values = set([row[col] for row in rows])
        for value in column_values:
            set1, set2 = divideset(rows, col, value)
            p = float(len(set1)) / len(rows)
            gain = current_score - p*scorefun(set1) - (1-p)*scorefun(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    if best_gain > 0:
        trueBranch = build_situation_memory_tree(best_sets[0], scorefun)
        falseBranch = build_situation_memory_tree(best_sets[1], scorefun)
        return SituationNode(col=best_criteria[0], value=best_criteria[1], tb=trueBranch, fb=falseBranch)
    else:
        return SituationNode(results=uniquecounts(rows), preserved_context=rows)

def modify_tree_table1(tree, input_object, input_sign, name_col=0):
    """
    👑 TABLE 1 DYNAMIC TREE MODIFICATION ENGINE
    Mutates terminal leaf nodes on the fly when new user instances arrive.
    """
    if tree.results is not None:
        # We are at a terminal leaf node. Evaluate the match boundaries.
        cached_row = tree.preserved_context[0]
        name_match = (str(input_object[name_col]) == str(cached_row[name_col]))
        
        # Calculate feature mismatch footprint across the vector parameters
        feature_match = True
        diff_col = -1
        diff_val = None
        for i in range(1, len(input_object) - 1):
            if str(input_object[i]) != str(cached_row[i]):
                feature_match = False
                diff_col = i
                diff_val = cached_row[i]
                break
                
        # Trigger explicit Action Steps based on Table 1 rules
        if name_match and feature_match and input_sign == "+":
            print("   📝 [TABLE 1 ACTION]: Step 1 Match -> Exact instance confirmed. Do nothing.")
            return tree
        elif name_match and not feature_match and input_sign == "+":
            print(f"   📝 [TABLE 1 ACTION]: Step 2 Match -> Name matches but features differ. Growing tree on column index {diff_col}.")
            # Grow tree branch dynamically to handle the new property split
            new_leaf = SituationNode(results={input_object[-1]: 1}, preserved_context=[input_object])
            if str(input_object[diff_col]) == str(diff_val):
                return SituationNode(col=diff_col, value=diff_val, tb=tree, fb=new_leaf)
            else:
                return SituationNode(col=diff_col, value=diff_val, tb=new_leaf, fb=tree)
        elif not name_match and feature_match and input_sign == "+":
            print(f"   📝 [TABLE 1 ACTION]: Step 5 Match -> Different Name but identical features. Growing tree on name test split.")
            new_leaf = SituationNode(results={input_object[-1]: 1}, preserved_context=[input_object])
            return SituationNode(col=name_col, value=cached_row[name_col], tb=tree, fb=new_leaf)
        elif not name_match and not feature_match and input_sign == "+":
            print(f"   📝 [TABLE 1 ACTION]: Step 6 Match -> Different Name and completely different features. Splitting tree on difference value: {diff_val}.")
            new_leaf = SituationNode(results={input_object[-1]: 1}, preserved_context=[input_object])
            return SituationNode(col=diff_col, value=diff_val, tb=tree, fb=new_leaf)
        else:
            print("   📝 [TABLE 1 ACTION]: Steps 4/7/8 Match -> Negative constraint boundary. Do nothing.")
            return tree

    # Recurse down the branches if we are at a non-terminal test node
    v = input_object[tree.col]
    if str(v) == str(tree.value):
        tree.tb = modify_tree_table1(tree.tb, input_object, input_sign, name_col)
    else:
        tree.fb = modify_tree_table1(tree.fb, input_object, input_sign, name_col)
    return tree

def print_situation_tree(tree, indent=''):
    if tree.results is not None:
        print(f" 📦 Leaf Label: {tree.results}")
    else:
        print(f" {tree.col}:{tree.value}?")
        print(indent + "T->", end='')
        print_situation_tree(tree.tb, indent + "  ")
        print(indent + "F->", end='')
        print_situation_tree(tree.fb, indent + "  ")

def classify_situation(observation, tree):
    if tree.results is not None: return tree.results, tree.preserved_context
    v = observation[tree.col]
    branch = tree.tb if str(v) == str(tree.value) else tree.fb
    return classify_situation(observation, branch)
