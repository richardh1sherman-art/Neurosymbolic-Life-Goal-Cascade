if __name__ == "__main__":
    inductor = RasiowaGridInductor(max_grid=10)
#   inductor = rasiowa_grid_inductor(max_grid=10)
    # 📝 Ingesting your exact file strings
    bias_file_content = """
    head_pred(f,2).
    body_pred(up,2).
    body_pred(down,2).
    body_pred(left,2).
    body_pred(right,2).
    direction(f,(in,out)).
    """
    
    examples_file_content = """
    pos(f(w(0,0),w(5,0))).
    neg(f(w(0,0),w(1,0))).
    neg(f(w(1,0),w(0,0))).
    neg(f(w(1,0),w(2,0))).
    neg(f(w(0,0),w(2,0))).
    neg(f(w(0,0),w(3,0))).
    neg(f(w(0,0),w(0,1))).
    neg(f(w(0,0),w(0,0))).
    """
    
    status, synthesized_prolog_program = inductor.induce_grid_program(
        exs_str=examples_file_content, 
        bias_str=bias_file_content
    )
    
    print("\n" + "="*75)
    print(f"🔮 RASIOWA ILP INDUCTION STATUS : {status}")
    print("="*75)
    print("📝 INDUCED COMPLIANT PROLOG PROGRAM:")
    print("-"*75)
    print(synthesized_prolog_program)
    print("="*75 + "\n")
