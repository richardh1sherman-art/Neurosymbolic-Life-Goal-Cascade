import os
import subprocess

class PragmaticContractAuditor:
    def __init__(self):
        self.grigorchuk_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/grigorchuk_planning_space"
        self.query_file = os.path.join(self.grigorchuk_dir, "run_breach_query.pl")

    def build_prolog_query_script(self):
        prolog_code = """
:- consult('kb.pl').

%% Mocking active situational instances directly for 2nd order logic verification
action_p_occurred(house_fire_dispatch).
has_permission_q(dispatcher_alert_rotation) :- fail. %% 🚨 Force a contract permission omission state

evaluate_system_breach :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG EVALUATOR: CHECKING 2ND ORDER PRAGMATIC CONTRACT INVARIANTS~n'),
    format('==================================================================================~n'),
    
    ( pragmatic_contract_breach(house_fire_dispatch, dispatcher_alert_rotation) ->
        format(' 🛑 [BREACH DETECTED]: Action [house_fire_dispatch] executed without permission constraint!~n')
    ;
        format(' 🟢 [CLEAR]: No social contract violations active in current manifold.~n')
    ),
    format('==================================================================================~n'),
    halt.
"""
        os.makedirs(os.path.dirname(self.query_file), exist_ok=True)
        with open(self.query_file, "w", encoding="utf-8") as f:
            f.write(prolog_code)

    def execute_audit(self):
        self.build_prolog_query_script()
        subprocess.run(
            ["swipl", "-q", "-g", "evaluate_system_breach", "run_breach_query.pl"],
            cwd=self.grigorchuk_dir,
            capture_output=False,
            text=True
        )

if __name__ == "__main__":
    # 🚨 FIXED: Removed the invalid colon modifier from the constructor instantiator block
    auditor = PragmaticContractAuditor()
    auditor.execute_audit()
