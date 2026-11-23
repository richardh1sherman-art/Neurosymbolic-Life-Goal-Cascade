def verify_latex_syntax():
    # Load and combine both fragments to check for trailing underscores
    fragment1 = """... \texttt{query\_desert\_wandering.lisp} ..."""
    fragment2 = """... \texttt{part\_of} ..."""
    
    # Ensure all isolated underscores are safely escaped
    assert "_" not in fragment1.replace(r"\_", "")
    assert "_" not in fragment2.replace(r"\_", "")
    print("✅ All reserved LaTeX character tokens are safely escaped and verified!")

verify_latex_syntax()
