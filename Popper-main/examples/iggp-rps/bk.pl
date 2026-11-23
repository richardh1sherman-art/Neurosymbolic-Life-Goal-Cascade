my_succ(0,1). my_succ(1,2). my_succ(2,3).
player(p1). player(p2).
action(paper). action(scissors). action(stone).
beats(paper,stone). beats(scissors,paper). beats(stone,scissors).
different(p1,p2). different(p2,p1).
does(1,p1,scissors). does(1,p2,stone). does(10,p1,stone). does(10,p2,stone). does(11,p1,stone). does(11,p2,paper).
does(12,p1,scissors). does(12,p2,paper). does(13,p1,scissors). does(13,p2,paper). does(15,p1,scissors). does(15,p2,paper).
does(16,p1,scissors). does(16,p2,stone). does(17,p1,scissors). does(17,p2,scissors). does(18,p1,scissors). does(18,p2,paper).
does(19,p1,stone). does(19,p2,stone). does(20,p1,scissors). does(20,p2,paper). does(21,p1,paper). does(21,p2,stone).
my_true_score(1,p1,0). my_true_score(1,p2,0). my_true_score(10,p1,1). my_true_score(10,p2,0).
my_true_score(11,p1,0). my_true_score(11,p2,0). my_true_score(12,p1,1). my_true_score(12,p2,1).
my_true_score(13,p1,1). my_true_score(13,p2,0). my_true_score(15,p1,0). my_true_score(15,p2,0).
my_true_score(16,p1,0). my_true_score(16,p2,0). my_true_score(17,p1,0). my_true_score(17,p2,0).
my_true_score(18,p1,0). my_true_score(18,p2,2). my_true_score(19,p1,0). my_true_score(19,p2,0).
my_true_score(20,p1,0). my_true_score(20,p2,0). my_true_score(21,p1,0). my_true_score(21,p2,0).
