import os

def evaluate_token(word):
    """
    Simulates the compiled rule inside linguistic_tier1/solution.pl:
    evaluate_vocab(linguistic_tier1, Word, POS) :- infon(Word, word_type, POS).
    """
    nouns = ["firefighter", "helicopter", "stove", "hydrant"]
    verbs = ["rescues", "deploys", "extinguishes", "charges"]
    adjectives = ["brave", "trapped", "hot", "live"]
    
    if word in nouns: return "noun"
    if word in verbs: return "verb"
    if word in adjectives: return "adjective"
    return "unknown"

def evaluate_sentence(sentence_str):
    """
    Simulates the compiled rule inside linguistic_tier2/solution.pl:
    sentence_valid(S) :- pos_1st=adj, pos_2nd=noun, pos_3rd=verb.
    """
    tokens = sentence_str.split()
    if len(tokens) != 3:
        return "INVALID_SYNTAX"
        
    pos1 = evaluate_token(tokens[0])
    pos2 = evaluate_token(tokens[1])
    pos3 = evaluate_token(tokens[2])
    
    if pos1 == "adjective" and pos2 == "noun" and pos3 == "verb":
        return "VALID_STRUCTURE"
    return "INVALID_SYNTAX"

def main():
    test_cases = [
        ("brave firefighter rescues", "Valid Template"),
        ("trapped helicopter deploys", "Valid Template"),
        ("rescues brave firefighter", "Invalid Syntax Pattern"),
        ("hot stove extinguishes", "OOD Unseen Sequence"),
        ("brave helicopter rescues", "OOD Unseen Sequence"),
        ("extinguishes hot firefighter", "OOD Invalid Sequence")
    ]

    print("=" * 85)
    print("📊 EVALUATION TABLE: STANDALONE SENTENCE GRAMMAR TEST")
    print("=" * 85)
    print(f"{'Sentence Target Profile':<30} | {'Expected Property':<24} | {'Tree Inference':<20} | {'Status'}")
    print("-" * 85)
    
    for query, expected in test_cases:
        res = evaluate_sentence(query)
        
        # Track clean passes vs blocks
        if "Invalid" in expected or "OOD Invalid" in expected:
            status = "✅ Clean Block" if res == "INVALID_SYNTAX" else "🚨 LEAKED FAULT"
        else:
            status = "✅ Clean Pass" if res == "VALID_STRUCTURE" else "🚨 BLOCKED FAULT"
            
        print(f"{query:<30} | {expected:<24} | {res:<20} | {status}")
        
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
