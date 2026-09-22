import os
import subprocess

class AnalogyTransferProver:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.query_file = os.path.join(self.grigorchuk_dir, "run_transfer_query.pl")

    def build_prolog_query_script(self):
        prolog_code = """
:- consult('kb.pl').

%% Asserting experimental context facts to validate 2nd order transfer properties
fact_holds_in_situation(prevent_via_friend_accompaniment, judith_mountain_rescue).

execute_transfer_evaluation :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG EVALUATOR: VERIFYING HIGH-ORDER ANALOGY FACT TRANSFERS~n'),
    format('==================================================================================~n'),
    
    % Test Reflexive Transfer: Mountain Rescue -> Kitchen Fire Setting
    ( transfer_fact_reflexive(prevent_via_friend_accompaniment, judith_mountain_rescue, george_kitchen_fire) ->
        format(' 🔄 [REFLEXIVE SUCCESS]: Fact transferred symmetrically to [george_kitchen_fire] (\u2218).~n')
    ;
        format(' ❌ Reflexive link failed.~n')
    ),
    
    % Test Transitive Chain: Mountain Rescue -> Kitchen Fire Setting -> Community Safety Rehearsal Workspace
    ( transfer_fact_transitive(prevent_via_friend_accompaniment, judith_mountain_rescue, george_kitchen_fire, community_safety_rehearsal) ->
        format(' 🔗 [TRANSITIVE SUCCESS]: Fact chained through to [community_safety_rehearsal] (\u2218).~n')
    ;
        format(' ❌ Transitive chain broken.~n')
    ),
    format('==================================================================================~n'),
    halt.
"""
        os.makedirs(os.path.dirname(self.query_file), exist_ok=True)
        with open(self.query_file, "w", encoding="utf-8") as f:
            f.write(prolog_code)

    def execute_proof(self):
        self.build_prolog_query_script()
        subprocess.run(
            ["swipl", "-q", "-g", "execute_transfer_evaluation", "run_transfer_query.pl"],
            cwd=self.grigorchuk_dir,
            capture_output=False,
            text=True
        )

if __name__ == "__main__":
    prover = AnalogyTransferProver()
    prover.execute_proof()
