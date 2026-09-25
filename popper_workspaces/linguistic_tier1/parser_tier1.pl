%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Algebraic Sensors and Story Problems
%% =================================================================

:- dynamic anti_pattern/1.
:- dynamic dsl_type/1.
:- dynamic story_sensor_fact/3.

%% --- TYPE DEFINITION LATTICE ---
dsl_type(void).   dsl_type(bool).   dsl_type(float).  dsl_type(vector).
dsl_type(object). dsl_type(action). dsl_type(list).  dsl_type(tile).
dsl_type(variable). %% 🚨 NEW: Algebraic symbol tracking

%% --- SYNTACTIC ANTI-PATTERN FILTERS (BANNED SCHEMAS) ---
anti_pattern(not(not(_))).
anti_pattern(if(not(_), _, _)).
anti_pattern(left(right(_))).
anti_pattern(right(left(_))).
anti_pattern(to(self)).
anti_pattern(eq(self, none)).
anti_pattern(maxDirection(alignment(#0, _))).
anti_pattern(plus(_, 0)).  %% 🚨 NEW ALGEBRAIC AP: Adding zero is redundant
anti_pattern(mult(_, 1)).  %% 🚨 NEW ALGEBRAIC AP: Multiplying by one is redundant

%% --- 5TH GRADE ALGEBRAIC STORY PROBLEMS SENSORS ---
% Problem: "Sam bought x boxes of pencils. Each box has 12 pencils. He gave away 5. He has 31 left."
story_sensor_fact(pencil_story, variable_token, x).
story_sensor_fact(pencil_story, scalar_multiplier, 12).
story_sensor_fact(pencil_story, scalar_subtractor, 5).
story_sensor_fact(pencil_story, target_equality, 31).

%% --- MASTER INTER-TREE DELEGATION RULES ---
part_of(Expression, anti_pattern, banned) :-
    anti_pattern(Expression), !.

part_of(StoryID, sensor_type, Metric) :-
    story_sensor_fact(StoryID, _, Metric).
