import subprocess
import os

class AdvancedDCGDiagnosticTester:
    def __init__(self):
        self.dcg_file = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl"

    def audit_sentence(self, sentence_text):
        prolog_query = f"consult('{self.dcg_file}'), (parse_sentence('{sentence_text}', Type, Name, Sign) -> format('Type: ~w | Concept: ~w | Sign: ~w', [Type, Name, Sign]) ; write('FAILED_SYNTAX')), halt."
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            return f"ERROR: {e}"

    def run_suite(self):
        print("=" * 95)
        print("🧪 TESTING TIER 1 ADVANCED RECURSIVE MULTI-WORD DCG PARSER SUITE")
        print("=" * 95)
        
        test_cases = [
            "alec figured blocks develop her mind",
            "alec couldnt afford new blocks",
            "she took tiny diamond stickers and stuck them",
            "an excavator severed the primary fiber link",
            "power surges corrupted the central train arrival display",
            "invalid sentence test word"
        ]
        
        for text in test_cases:
            res = self.audit_sentence(text)
            print(f"📥 Input Text ──➔ \"{text}\"")
            print(f"   └── Prolog Parse Return ──➔ {res}\n")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    tester = AdvancedDCGDiagnosticTester()
    tester.run_suite()
