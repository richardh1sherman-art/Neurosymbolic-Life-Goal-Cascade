import os
import subprocess

class ApexForestVerifier:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples/grigorchuk_planning_space"
        self.test_runner_file = os.path.join(self.grigorchuk_dir, "verify_forest_closure.pl")

    def build_prolog_test_runner(self):
        prolog_code = """
:- consult('kb.pl').
:- consult('/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl').

verify_apex_dispatch(ProblemID) :-
    ( part_of(ProblemID, apex_routing, Target) ->
        format(' [VALID] Apex Tree #0 Dispatch Layer Closed | Problem Path Maps to: ~w (\u2218).', [Target])
    ;
        write(' [ERROR] Apex routing token signature missing from database scope (\u2022).')
    ).

verify_tree30_parthood(TaskToken) :-
    ( part_of(TaskToken, tree_30_routing, SubTree) ->
        format(' [VALID] Tree #30 Parthood Layer Closed | Target Sub-Network Module: ~w (\u2218).', [SubTree])
    ;
        write(' [ERROR] Task token parthood signature missing from Tree #30 registry (\u2022).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: GLOBAL APEX AND PARTHOOD DISPATCH AUDIT~n'),
    format('==================================================================================~n'),
    
    verify_apex_dispatch(monkey_bananas), format('~n'),
    verify_apex_dispatch(dynamic_sds_swarm), format('~n'),
    
    format('----------------------------------------------------------------------------------~n'),
    verify_tree30_parthood(collision_check), format('~n'),
    verify_tree30_parthood(signal_mesh), format('~n'),
    verify_tree30_parthood(load_balancing), format('~n'),
    
    format('==================================================================================~n'),
    halt.
"""
        os.makedirs(os.path.dirname(self.test_runner_file), exist_ok=True)
        with open(self.test_runner_file, "w", encoding="utf-8") as f:
            f.write(prolog_code)

    def execute_swipl_process(self):
        self.build_prolog_test_runner()
        result = subprocess.run(
            ["swipl", "-q", "-g", "execute_verification_audit", "verify_forest_closure.pl"],
            cwd=self.grigorchuk_dir,
            capture_output=True,
            text=True
        )
        print(result.stdout)

if __name__ == "__main__":
    engine = ApexForestVerifier()
    engine.execute_swipl_process()
