:- discontiguous infon/3.
:- discontiguous part_of/2.

infon(f_pos, batteries, live). infon(f_pos, bulb, works). infon(f_pos, switch, on).
infon(f_neg1, batteries, dead). infon(f_neg1, bulb, works). infon(f_neg1, switch, on).
infon(f_neg2, batteries, live). infon(f_neg2, bulb, broken). infon(f_neg2, switch, on).
