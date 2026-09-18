import os
import subprocess

class GrigorchukWeightedVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_weighted_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('exs.pl').

query_path_safely(StoryID, Cost) :-
    validate_path_minor(start_node, goal_vertex, StoryID, Cost), !.
query_path_safely(StoryID, Cost) :-
    validate_path_minor(station, goal_vertex, StoryID, Cost), !.
query_path_safely(StoryID, Cost) :-
    validate_path_minor(airport_gate, goal_vertex, StoryID, Cost), !.

evaluate_story_cost(StoryID) :-
    ( query_path_safely(StoryID, Cost) ->
        format(' [VALID] Path Minor Clear | Grigorchuk Cost: ~w (\u2218).', [Cost])
    ;
        write(' [BLOCKED] Decalogue Violation Severed Path (\u2022).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: GRIGORCHUK COST MATRIX CLOSURE~n'),
    format('==================================================================================~n'),
    
    format('   ➔ Story [pierre_story_s1]       ──➔ STATUS:'), evaluate_story_cost(pierre_story_s1), format('~n'),
    format('   ➔ Story [pierre_story_s2]       ──➔ STATUS:'), evaluate_story_cost(pierre_story_s2), format('~n'),
    format('   ➔ Story [pierre_story_s2_prime] ──➔ STATUS:'), evaluate_story_cost(pierre_story_s2_prime), format('~n'),
    format('   ➔ Story [alec_story_s2]         ──➔ STATUS:'), evaluate_story_cost(alec_story_s2), format('~n'),
    format('   ➔ Story [alec_story_s2_prime]   ──➔ STATUS:'), evaluate_story_cost(alec_story_s2_prime), format('~n'),
    format('   ➔ Story [ana_story_s2]          ──➔ STATUS:'), evaluate_story_cost(ana_story_s2), format('~n'),
    format('   ➔ Story [ana_story_s2_prime]    ──➔ STATUS:'), evaluate_story_cost(ana_story_s2_prime), format('~n'),
    format('   ➔ Story [john_story_s1]         ──➔ STATUS:'), evaluate_story_cost(john_story_s1), format('~n'),
    format('   ➔ Story [moses_sovereign_flaw]  ──➔ STATUS:'), evaluate_story_cost(moses_sovereign_flaw), format('~n'),
    format('   ➔ Story [david_sovereign_flaw]  ──➔ STATUS:'), evaluate_story_cost(david_sovereign_flaw), format('~n'),
    format('   ➔ Story [paul_sovereign_flaw]   ──➔ STATUS:'), evaluate_story_cost(paul_sovereign_flaw), format('~n'),
    
    format('==================================================================================~n'),
    halt.
"""
        os.makedirs(os.path.dirname(self.test_runner_file), exist_ok=True)
        with open(self.test_runner_file, "w", encoding="utf-8") as f:
            f.write(prolog_code)

    def execute_swipl_process(self):
        self.build_prolog_test_runner()
        result = subprocess.run(
            ["swipl", "-q", "-g", "execute_verification_audit", "verify_weighted_closure.pl"],
            cwd=self.grigorchuk_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    engine = GrigorchukWeightedVerifier()
    engine.execute_swipl_process()
