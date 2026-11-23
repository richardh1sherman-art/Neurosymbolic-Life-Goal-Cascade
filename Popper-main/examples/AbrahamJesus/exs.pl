% =====================================================================
% FILENAME: exs.pl
% PURPOSE: Training Examples for the Abraham/Jesus Analogy Tree
%          Maps positive and negative states to guide induction.
% =====================================================================

% --- Positive Examples (Success at all levels) ---
pos(state_abraham_success).
pos(state_jesus_success).

% --- Negative Examples (Failures at Level 1: Physical Objects) ---
neg(state_abraham_no_knife).
neg(state_jesus_no_cross).

% --- Negative Examples (Failures at Level 2: Spiritual Execution) ---
neg(state_abraham_refuses).
neg(state_jesus_saves_himself).
