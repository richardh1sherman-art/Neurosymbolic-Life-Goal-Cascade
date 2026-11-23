%% Tier 2 Background Knowledge - Mapping Structural Sequence Tokens
part_of_selector(pos_1st, sentence_alpha, brave).
part_of_selector(pos_2nd, sentence_alpha, firefighter).
part_of_selector(pos_3rd, sentence_alpha, rescues).

part_of_selector(pos_1st, sentence_beta, trapped).
part_of_selector(pos_2nd, sentence_beta, helicopter).
part_of_selector(pos_3rd, sentence_beta, deploys).

%% Local Inheritance Subroutine Stubs
evaluate_vocab(linguistic_tier1, brave, adjective).
evaluate_vocab(linguistic_tier1, firefighter, noun).
evaluate_vocab(linguistic_tier1, rescues, verb).
evaluate_vocab(linguistic_tier1, trapped, adjective).
evaluate_vocab(linguistic_tier1, helicopter, noun).
evaluate_vocab(linguistic_tier1, deploys, verb).
