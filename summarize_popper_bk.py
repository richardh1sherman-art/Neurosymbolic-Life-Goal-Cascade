import os
import re
import collections

class PopperBackgroundSummarizer:
    """
    Applies approximation logic to summarize the structure and distribution
    of predicates inside Popper background knowledge files (bk.pl).
    """
    def __init__(self, examples_root="Popper-main/examples"):
        self.examples_root = examples_root

    def analyze_bk_file(self, folder_name):
        bk_path = os.path.join(self.examples_root, folder_name, "bk.pl")
        if not os.path.exists(bk_path):
            return None

        with open(bk_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Clean out comments and blank lines
        lines = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("%")]
        
        predicate_counts = collections.Counter()
        arity_map = {}
        example_arguments = {}

        for line in lines:
            # Match standard Prolog fact syntax: predicate_name(arg1, arg2...)
            match = re.match(r"^([a-z0-9_]+)\((.+?)\)\s*\:-|\.$|^([a-z0-9_]+)\((.+?)\)\.", line)
            if match:
                pred = match.group(1) or match.group(3)
                args_str = match.group(2) or match.group(4)
                if not pred:
                    continue
                
                args = [a.strip() for a in args_str.split(",")]
                arity = len(args)
                
                predicate_counts[f"{pred}/{arity}"] += 1
                arity_map[pred] = arity
                if f"{pred}/{arity}" not in example_arguments:
                    example_arguments[f"{pred}/{arity}"] = args_str

        return {
            "total_facts": sum(predicate_counts.values()),
            "distinct_signatures": len(predicate_counts),
            "distribution": dict(predicate_counts),
            "examples": example_arguments
        }

    def generate_global_summary_report(self):
        if not os.path.exists(self.examples_root):
            return f"❌ Root benchmarks folder not found at path: {self.examples_root}"

        folders = sorted([f for f in os.listdir(self.examples_root) if os.path.isdir(os.path.join(self.examples_root, f))])
        
        report_lines = []
        report_lines.append("=" * 85)
        report_lines.append("🔬 NEURO-SYMBOLIC TOPOLOGICAL BACKGROUND KNOWLEDGE SUMMARY REPORT")
        report_lines.append("=" * 85)
        report_lines.append(f"Target Base Source Hierarchy Path: '{self.examples_root}'\n")

        for folder in folders:
            stats = self.analyze_bk_file(folder)
            if not stats:
                continue

            report_lines.append(f"📁 [DOMAIN WORKSPACE]: {folder}")
            report_lines.append(f"   🔹 Total Ground Facts: {stats['total_facts']}")
            report_lines.append(f"   🔹 Distinct Predicate Signatures: {stats['distinct_signatures']}")
            report_lines.append("   🔹 Topological Equivalence Class Dispersions:")
            
            for sig, count in sorted(stats["distribution"].items()):
                sample = stats["examples"][sig]
                report_lines.append(f"      ▪️ {sig:<18} -> Count: {count:<6} | Sample Fact Infon Shape: {sig.split('/')[0]}({sample})")
            report_lines.append("-" * 85)

        return "\n".join(report_lines)

if __name__ == "__main__":
    summarizer = PopperBackgroundSummarizer()
    print(summarizer.generate_global_summary_report())
